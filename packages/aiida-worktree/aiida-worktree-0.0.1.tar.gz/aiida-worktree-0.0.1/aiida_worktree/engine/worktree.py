"""AiiDA workflow components: WorkTree."""
from __future__ import annotations

import collections.abc
import functools
import logging
import typing as t

from plumpy.persistence import auto_persist
from plumpy.process_states import Continue, Wait
from plumpy.workchains import _PropagateReturn
from plumpy.workchains import WorkChainSpec as PlumpyWorkChainSpec

from aiida.common import exceptions
from aiida.common.extendeddicts import AttributeDict
from aiida.common.lang import override
from aiida import orm
from aiida.orm import Node, ProcessNode, WorkflowNode
from aiida.orm.utils import load_node


from aiida.engine.processes.exit_code import ExitCode
from aiida.engine.processes.process import Process, ProcessState
from aiida.engine.processes.process_spec import ProcessSpec

from aiida.engine.processes.workchains.awaitable import (
    Awaitable,
    AwaitableAction,
    AwaitableTarget,
    construct_awaitable,
)
from aiida.engine.processes.workchains.workchain import Protect, WorkChainSpec
from aiida.engine import run_get_node

from os.path import splitext
import yaml


if t.TYPE_CHECKING:
    from aiida.engine.runners import Runner  # pylint: disable=unused-import

__all__ = "WorkTree"


def get_input_links(node_name, links):
    inputs = []
    for link in links:
        if link["to_node"] == node_name:
            inputs.append(link)
    return inputs


class WorkTreeSpec(ProcessSpec, PlumpyWorkChainSpec):
    pass


@auto_persist("_awaitables")
class WorkTree(Process, metaclass=Protect):
    """The `WorkTree` class is used to construct workflows in AiiDA."""

    _node_class = WorkflowNode
    _spec_class = WorkTreeSpec
    _CONTEXT = "CONTEXT"

    def __init__(
        self,
        inputs: dict | None = None,
        logger: logging.Logger | None = None,
        runner: "Runner" | None = None,
        enable_persistence: bool = True,
    ) -> None:
        """Construct a WorkChain instance.

        Construct the instance only if it is a sub class of `WorkChain`, otherwise raise `InvalidOperation`.

        :param inputs: work chain inputs
        :param logger: aiida logger
        :param runner: work chain runner
        :param enable_persistence: whether to persist this work chain

        """

        super().__init__(inputs, logger, runner, enable_persistence=enable_persistence)

        self._awaitables: list[Awaitable] = []
        self._context = AttributeDict()

    @classmethod
    def spec(cls) -> WorkChainSpec:
        return super().spec()  # type: ignore[return-value]

    @classmethod
    def define(cls, spec):
        super().define(spec)
        spec.input("input_file", valid_type=orm.SinglefileData, required=False)
        spec.input_namespace("nt", dynamic=True, required=False)
        spec.input_namespace("input_nodes", dynamic=True, required=False)
        spec.exit_code(2, "ERROR_SUBPROCESS", message="A subprocess has failed.")

        spec.output_namespace("results", dynamic=True)
        #
        spec.exit_code(
            201, "UNKNOWN_MESSAGE_TYPE", message="The message type is unknown."
        )
        spec.exit_code(202, "UNKNOWN_NODE_TYPE", message="The node type is unknown.")
        #
        spec.exit_code(
            301,
            "OUTPUS_NOT_MATCH_RESULTS",
            message="The outputs of the process do not match the results.",
        )
        spec.exit_code(
            302,
            "NODE_FAILED",
            message="Some of the nodes failed.",
        )

    @property
    def node(self) -> WorkflowNode:
        return super().node  # type: ignore

    @property
    def ctx(self) -> AttributeDict:
        """Get the context."""
        return self._context

    @override
    def save_instance_state(self, out_state, save_context):
        """Save instance state.

        :param out_state: state to save in

        :param save_context:
        :type save_context: :class:`!plumpy.persistence.LoadSaveContext`

        """
        super().save_instance_state(out_state, save_context)
        # Save the context
        out_state[self._CONTEXT] = self.ctx

    @override
    def load_instance_state(self, saved_state, load_context):
        super().load_instance_state(saved_state, load_context)
        # Load the context
        self._context = saved_state[self._CONTEXT]

        self.set_logger(self.node.logger)

        if self._awaitables:
            self._action_awaitables()

    @Protect.final
    def on_run(self):
        super().on_run()

    def _resolve_nested_context(self, key: str) -> tuple[AttributeDict, str]:
        """
        Returns a reference to a sub-dictionary of the context and the last key,
        after resolving a potentially segmented key where required sub-dictionaries are created as needed.

        :param key: A key into the context, where words before a dot are interpreted as a key for a sub-dictionary
        """
        ctx = self.ctx
        ctx_path = key.split(".")

        for index, path in enumerate(ctx_path[:-1]):
            try:
                ctx = ctx[path]
            except KeyError:  # see below why this is the only exception we have to catch here
                ctx[
                    path
                ] = AttributeDict()  # create the sub-dict and update the context
                ctx = ctx[path]
                continue

            # Notes:
            # * the first ctx (self.ctx) is guaranteed to be an AttributeDict, hence the post-"dereference" checking
            # * the values can be many different things: on insertion they are either AtrributeDict, List or Awaitables
            #   (subclasses of AttributeDict) but after resolution of an Awaitable this will be the value itself
            # * assumption: a resolved value is never a plain AttributeDict, on the other hand if a resolved Awaitable
            #   would be an AttributeDict we can append things to it since the order of tasks is maintained.
            if type(ctx) != AttributeDict:  # pylint: disable=C0123
                raise ValueError(
                    f"Can not update the context for key `{key}`:"
                    f' found instance of `{type(ctx)}` at `{".".join(ctx_path[:index+1])}`, expected AttributeDict'
                )

        return ctx, ctx_path[-1]

    def _insert_awaitable(self, awaitable: Awaitable) -> None:
        """Insert an awaitable that should be terminated before before continuing to the next step.

        :param awaitable: the thing to await
        """
        ctx, key = self._resolve_nested_context(awaitable.key)

        # Already assign the awaitable itself to the location in the context container where it is supposed to end up
        # once it is resolved. This is especially important for the `APPEND` action, since it needs to maintain the
        # order, but the awaitables will not necessarily be resolved in the order in which they are added. By using the
        # awaitable as a placeholder, in the `_resolve_awaitable`, it can be found and replaced by the resolved value.
        if awaitable.action == AwaitableAction.ASSIGN:
            ctx[key] = awaitable
        elif awaitable.action == AwaitableAction.APPEND:
            ctx.setdefault(key, []).append(awaitable)
        else:
            raise AssertionError(f"Unsupported awaitable action: {awaitable.action}")

        self._awaitables.append(
            awaitable
        )  # add only if everything went ok, otherwise we end up in an inconsistent state
        self._update_process_status()

    def _resolve_awaitable(self, awaitable: Awaitable, value: t.Any) -> None:
        """Resolve an awaitable.

        Precondition: must be an awaitable that was previously inserted.

        :param awaitable: the awaitable to resolve
        """

        ctx, key = self._resolve_nested_context(awaitable.key)

        if awaitable.action == AwaitableAction.ASSIGN:
            ctx[key] = value
        elif awaitable.action == AwaitableAction.APPEND:
            # Find the same awaitable inserted in the context
            container = ctx[key]
            for index, placeholder in enumerate(container):
                if (
                    isinstance(placeholder, Awaitable)
                    and placeholder.pk == awaitable.pk
                ):
                    container[index] = value
                    break
            else:
                raise AssertionError(
                    f"Awaitable `{awaitable.pk} was not found in `ctx.{awaitable.key}`"
                )
        else:
            raise AssertionError(f"Unsupported awaitable action: {awaitable.action}")

        awaitable.resolved = True
        self._awaitables.remove(
            awaitable
        )  # remove only if everything went ok, otherwise we may lose track

        if not self.has_terminated():
            # the process may be terminated, for example, if the process was killed or excepted
            # then we should not try to update it
            self._update_process_status()

    @Protect.final
    def to_context(self, **kwargs: Awaitable | ProcessNode) -> None:
        """Add a dictionary of awaitables to the context.

        This is a convenience method that provides syntactic sugar, for a user to add multiple intersteps that will
        assign a certain value to the corresponding key in the context of the work chain.
        """
        for key, value in kwargs.items():
            awaitable = construct_awaitable(value)
            awaitable.key = key
            self._insert_awaitable(awaitable)

    def _update_process_status(self) -> None:
        """Set the process status with a message accounting the current sub processes that we are waiting for."""
        if self._awaitables:
            status = f"Waiting for child processes: {', '.join([str(_.pk) for _ in self._awaitables])}"
            self.node.set_process_status(status)
        else:
            self.node.set_process_status(None)

    @override
    def run(self) -> t.Any:
        self.report("Run: ")
        self.setup()
        return self._do_step()

    def _do_step(self) -> t.Any:
        """Execute the next step in the outline and return the result.

        If any awaitables were created, the process will enter in the Wait state,
        otherwise it will go to Continue.
        """

        self._awaitables = []
        result: t.Any = None

        try:
            self.launch_worktree()
        except _PropagateReturn as exception:
            finished, result = True, exception.exit_code
        else:
            finished = self.is_worktree_finished()

        # If the worktree is finished or the result is an ExitCode, we exit by returning
        if finished:
            result = self.finalize()
            return result

        if self._awaitables:
            return Wait(self._do_step, "Waiting before next step")

        return Continue(self._do_step)

    def _store_nodes(self, data: t.Any) -> None:
        """Recurse through a data structure and store any unstored nodes that are found along the way

        :param data: a data structure potentially containing unstored nodes
        """
        if isinstance(data, Node) and not data.is_stored:
            data.store()
        elif isinstance(data, collections.abc.Mapping):
            for _, value in data.items():
                self._store_nodes(value)
        elif isinstance(data, collections.abc.Sequence) and not isinstance(data, str):
            for value in data:
                self._store_nodes(value)

    @override
    @Protect.final
    def on_exiting(self) -> None:
        """Ensure that any unstored nodes in the context are stored, before the state is exited

        After the state is exited the next state will be entered and if persistence is enabled, a checkpoint will
        be saved. If the context contains unstored nodes, the serialization necessary for checkpointing will fail.
        """
        super().on_exiting()
        try:
            self._store_nodes(self.ctx)
        except Exception:  # pylint: disable=broad-except
            # An uncaught exception here will have bizarre and disastrous consequences
            self.logger.exception("exception in _store_nodes called in on_exiting")

    @Protect.final
    def on_wait(self, awaitables: t.Sequence[t.Awaitable]):
        """Entering the WAITING state."""
        super().on_wait(awaitables)
        if self._awaitables:
            self._action_awaitables()
        else:
            self.call_soon(self.resume)

    def _action_awaitables(self) -> None:
        """Handle the awaitables that are currently registered with the work chain.

        Depending on the class type of the awaitable's target a different callback
        function will be bound with the awaitable and the runner will be asked to
        call it when the target is completed
        """
        for awaitable in self._awaitables:
            if awaitable.target == AwaitableTarget.PROCESS:
                callback = functools.partial(
                    self.call_soon, self._on_awaitable_finished, awaitable
                )
                self.runner.call_on_process_finish(awaitable.pk, callback)
            else:
                assert f"invalid awaitable target '{awaitable.target}'"

    def _on_awaitable_finished(self, awaitable: Awaitable) -> None:
        """Callback function, for when an awaitable process instance is completed.

        The awaitable will be effectuated on the context of the work chain and removed from the internal list. If all
        awaitables have been dealt with, the work chain process is resumed.

        :param awaitable: an Awaitable instance
        """
        self.logger.info(
            "received callback that awaitable %d has terminated", awaitable.pk
        )

        try:
            node = load_node(awaitable.pk)
        except (exceptions.MultipleObjectsError, exceptions.NotExistent):
            raise ValueError(
                f"provided pk<{awaitable.pk}> could not be resolved to a valid Node instance"
            )

        if awaitable.outputs:
            value = {
                entry.link_label: entry.node for entry in node.base.links.get_outgoing()
            }
        else:
            value = node  # type: ignore

        self._resolve_awaitable(awaitable, value)

        if self.state == ProcessState.WAITING and not self._awaitables:
            self.resume()

    def setup(self):
        from scinode.utils.nt_analysis import ConnectivityAnalysis

        self.ctx.results = dict()
        self.ctx.input_nodes = dict()
        if "input_file" in self.inputs:
            ext = splitext(self.inputs["input_file"].filename)[1]
            with self.inputs["input_file"].open(mode="r") as f:
                if ext == ".yaml":
                    ntdata = yaml.safe_load(f)
                else:
                    raise Exception("Please use a yaml file.")
        elif "nt" in self.inputs:
            ntdata = self.inputs["nt"]
        else:
            raise Exception("Please set input!")

        # ntdata = jsonref.JsonRef.replace_refs(tntdata, loader = JsonYamlLoader())
        self.ctx.worktree = ntdata
        nodes = {}
        for name, node in ntdata["nodes"].items():
            inputs = get_input_links(name, ntdata["links"])
            node["inputs"] = inputs
            nodes[name] = node
        self.ctx.nodes = nodes
        self.ctx.links = ntdata["links"]
        self.ctx.ctrl_links = ntdata["ctrl_links"]
        # init
        for name, node in self.ctx.nodes.items():
            node["state"] = "CREATED"
            node["process"] = None
        #
        nc = ConnectivityAnalysis(ntdata)
        self.ctx.connectivity = nc.build_connectivity()
        self.ctx.msgs = []
        # self.node.set_process_label(f"WorkTree: {self.ctx.worktree['name']}")

    def launch_worktree(self):
        self.report("Lanch worktree.")
        node_to_run = []
        for name, node in self.ctx.nodes.items():
            # update node state
            if node["state"] in ["RUNNING", "FINISHED", "FAILED", "SKIPPED"]:
                continue
            ready, output = self.check_parent_state(name)
            if ready:
                node_to_run.append(name)
        #
        print("node_to_run:", node_to_run)
        self.run_nodes(node_to_run)

    def is_worktree_finished(self):
        flag = True
        # print("is_worktree_finished:")
        for name, node in self.ctx.nodes.items():
            print(name, node["state"])
            # if calc process, and has a process, check process state
            if (
                node["metadata"]["node_type"]
                in [
                    "calcfunction",
                    "workfunction",
                    "calcjob",
                    "workchain",
                ]
                and node["state"] == "RUNNING"
            ):
                if node.get("process"):
                    state = node["process"].process_state.value.upper()
                    print(node["name"], state)
                    if state == "FINISHED":
                        node["state"] = state
                        node["results"] = node["process"].outputs
                        self.ctx.results[name] = node["results"]
                        self.ctx.nodes[name]["state"] = "FINISHED"
                        print(f"Node: {name} finished.")
                    elif state == "EXCEPTED":
                        node["state"] = state
                        node["results"] = node["process"].outputs
                        self.ctx.results[name] = node["results"]
                        self.ctx.nodes[name]["state"] = "FAILED"
                        # set child state to FAILED
                        self.set_node_state(
                            self.ctx.connectivity["child_node"][name], "FAILED"
                        )
                        print(f"Node: {name} failed.")
            if node["state"] in ["RUNNING", "CREATED", "READY"]:
                flag = False
        return flag

    def run_nodes(self, names):
        """Run node
        Here we use ToContext to pass the results of the run to the next step.
        This will force the engine to wait for all the submitted processes to
        finish before continuing to the next step.

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """
        from aiida_worktree.utils import (
            get_executor,
            create_data_node,
            update_nested_dict_with_special_keys,
        )

        for name in names:
            # print("-" * 60)
            node = self.ctx.nodes[name]
            print(f"Run node: {name}, type: {node['metadata']['node_type']}")
            self.report(f"Run node: {name}, type: {node['metadata']['node_type']}")
            # print("Run node: ", name)
            # print("executor: ", node["executor"])
            executor, _ = get_executor(node["executor"])
            args, kwargs = self.get_inputs(node)
            # update the port namespace
            kwargs = update_nested_dict_with_special_keys(kwargs)
            print("args: ", args)
            print("kwargs: ", kwargs)
            # kwargs["meta.label"] = name
            # output must be a Data type or a mapping of {string: Data}
            node["results"] = {}
            if node["metadata"]["node_type"] == "node":
                print("node  type: node.")
                if isinstance(args[0], orm.Node):
                    results = args[0]
                else:
                    results = executor(*args, **kwargs)
                node["process"] = results
                node["results"] = {node["outputs"][0]["name"]: results}
                self.ctx.input_nodes[name] = results
                self.ctx.nodes[name]["state"] = "FINISHED"
                # ValueError: attempted to add an input link after the process node was already stored.
                # self.node.base.links.add_incoming(results, "INPUT_WORK", name)
            elif node["metadata"]["node_type"] == "data":
                print("node  type: data.")
                results = create_data_node(executor, args, kwargs)
                node["results"] = {node["outputs"][0]["name"]: results}
                node["process"] = results
                self.ctx.results[name] = results
                self.ctx.nodes[name]["state"] = "FINISHED"
            elif node["metadata"]["node_type"] in ["calcfunction", "workfunction"]:
                print("node  type: calcfunction/workfunction.")
                kwargs.setdefault("metadata", {})
                kwargs["metadata"].update({"call_link_label": name})
                try:
                    results, process = run_get_node(executor, *args, **kwargs)
                    # only one output
                    if isinstance(results, orm.Data):
                        results = {node["outputs"][0]["name"]: results}
                    node["results"] = results
                    # print("results: ", results)
                    node["process"] = process
                    self.ctx.nodes[name]["state"] = "FINISHED"
                except Exception as e:
                    print(e)
                    self.ctx.nodes[name]["state"] = "FAILED"
                    # set child state to FAILED
                    self.set_node_state(
                        self.ctx.connectivity["child_node"][name], "FAILED"
                    )
                    print(f"Node: {name} failed.")
            elif node["metadata"]["node_type"] in ["calcjob", "workchain"]:
                # process = run_get_node(executor, *args, **kwargs)
                print("node  type: calcjob/workchain.")
                kwargs.setdefault("metadata", {})
                kwargs["metadata"].update({"call_link_label": name})
                process = self.submit(executor, *args, **kwargs)
                node["process"] = process
                self.ctx.nodes[name]["state"] = "RUNNING"
                return self.to_context(process=process)
            elif node["metadata"]["node_type"] in ["Normal"]:
                print("node  type: Normal.")
                # normal function does not have a process
                if "ctx" in node["metadata"]["kwargs"]:
                    self.ctx.node_name = name
                    kwargs.update({"ctx": self.ctx})
                results = executor(*args, **kwargs)
                # node["process"] = results
                if isinstance(results, tuple):
                    if len(node["outputs"]) != len(results):
                        return self.exit_codes.OUTPUS_NOT_MATCH_RESULTS
                    for i in range(len(node["outputs"])):
                        node["results"][node["outputs"][i]["name"]] = results[i]
                else:
                    node["results"][node["outputs"][0]["name"]] = results
                self.ctx.input_nodes[name] = results
                self.ctx.nodes[name]["state"] = "FINISHED"
                # print("result from node: ", node["results"])
            else:
                print("node  type: unknown.")
                # self.report("Unknow node type {}".format(node["metadata"]["node_type"]))
                return self.exit_codes.UNKNOWN_NODE_TYPE

    def get_inputs(self, node):
        args = []
        kwargs = {}
        properties = node.get("properties", {})
        # TODO: check if input is linked, otherwise use the property value
        for name in node["metadata"].get("args", {}):
            has_input_link = False
            for input in node["inputs"]:
                if name == input["to_socket"]:
                    args.append(
                        self.ctx.nodes[input["from_node"]]["results"][
                            input["from_socket"]
                        ]
                    )
                    has_input_link = True
                    break
            if not has_input_link and name in properties:
                args.append(properties[name]["value"])
        for name in node["metadata"].get("kwargs", {}):
            if name in properties:
                kwargs[name] = properties[name]["value"]
            for input in node["inputs"]:
                if name == input["to_socket"]:
                    # print("input: ", input)
                    if self.ctx.nodes[input["from_node"]]["results"] is None:
                        kwargs[name] = None
                    else:
                        kwargs[name] = self.ctx.nodes[input["from_node"]]["results"][
                            input["from_socket"]
                        ]
        return args, kwargs

    def check_node_state(self, name):
        """Check node states.

        - if all input nodes finished, launch node
        - if node is a scatter node, check if all scattered nodes finished
        """
        # print(f"    Check node {name} state: ")
        if self.ctx.nodes[name]["state"] in ["CREATED", "WAITING"]:
            ready, output = self.check_parent_state(name)
            if ready:
                # print(f"    Node {name} is ready to launch.")
                self.ctx.msgs.append(f"node,{name}:action:LAUNCH")
        elif self.ctx.nodes[name]["state"] in ["SCATTERED"]:
            state, action = self.check_scattered_state(name)
            self.ctx.msgs.append(f"node,{name}:state:{state}")
        else:
            # print(f"    Node {name} is in state {self.ctx.nodes[name]['state']}")
            pass

    def check_parent_state(self, name):
        node = self.ctx.nodes[name]
        inputs = node.get("inputs", None)
        ready = True
        if inputs is None:
            return ready
        else:
            # check the control links first
            input_links = self.ctx.connectivity["ctrl_input_link"][node["name"]]
            if input_links.get("Entry", {}):
                states = [self.ctx.ctrl_links[i]["state"] for i in input_links["Entry"]]
                if True not in states:
                    ready = False
                    return ready, f"{name}, input entry control link is not FINISHED"
            for input in inputs:
                # print("    input, ", input["from_node"], self.ctx.nodes[input["from_node"]]["state"])
                if self.ctx.nodes[input["from_node"]]["state"] not in [
                    "FINISHED",
                    "SKIPPED",
                    "FAILED",
                ]:
                    print(
                        f"    {name}: Input node {input['from_node']}, {self.ctx.nodes[input['from_node']]['state']} ."
                    )
                    ready = False
                    return (
                        ready,
                        f"{name}, input: {input['from_node']} is {self.ctx.nodes[input['from_node']]['state']}",
                    )
        return ready, None

    def set_node_state(self, names, value):
        """Set node state"""
        for name in names:
            self.ctx.nodes[name]["state"] = value

    def finalize(self):
        """"""
        self.out("results", self.ctx.results)
        self.report("Finalize")
        print("Finalize")
        for name, node in self.ctx.nodes.items():
            if node["state"] == "FAILED":
                print(f"    Node {name} failed.")
                return self.exit_codes.NODE_FAILED
