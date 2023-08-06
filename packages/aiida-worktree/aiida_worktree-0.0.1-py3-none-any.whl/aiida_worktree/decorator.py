from typing import Any
from scinode.utils.node import get_executor
from aiida.engine.processes.functions import calcfunction, workfunction
from aiida.engine.processes.calcjobs import CalcJob
from aiida.engine.processes.workchains import WorkChain
from aiida.orm.nodes.process.calculation.calcfunction import CalcFunctionNode
from aiida.orm.nodes.process.workflow.workfunction import WorkFunctionNode
from aiida.engine.processes.ports import PortNamespace


def add_input_recursive(inputs, port, prefix=None):
    """Add input recursively."""
    if prefix is None:
        port_name = port.name
    else:
        port_name = f"{prefix}.{port.name}"
    if isinstance(port, PortNamespace):
        inputs.append(["General", port_name, ["General", {"default": {}}]])
        for key, value in port.items():
            add_input_recursive(inputs, value, prefix=port_name)
    else:
        inputs.append(["General", port_name])
    return inputs


def register_node(ndata):
    """Register a node from a AiiDA component."""
    from scinode.utils.decorator import register_node as register_scinode_node

    path, executor_name, = ndata.pop(
        "path"
    ).rsplit(".", 1)
    ndata["executor"] = {"path": path, "name": executor_name}
    executor, type = get_executor(ndata["executor"])
    # print(executor)
    if issubclass(executor, CalcJob):
        ndata["node_type"] = "calcjob"
    elif issubclass(executor, WorkChain):
        ndata["node_type"] = "workchain"
    else:
        ndata["node_type"] = "normal"
    inputs = []
    outputs = []
    spec = executor.spec()
    for key, port in spec.inputs.ports.items():
        add_input_recursive(inputs, port)
    kwargs = [input[1] for input in inputs]
    for key, port in spec.outputs.ports.items():
        outputs.append(["General", port.name])
    # print("kwargs: ", kwargs)
    ndata["kwargs"] = kwargs
    ndata["inputs"] = inputs
    ndata["outputs"] = outputs
    identifier = ndata.pop("identifier", ndata["executor"]["name"])
    node = register_scinode_node(identifier, **ndata)
    return node


# decorator with arguments indentifier, args, kwargs, properties, inputs, outputs, executor
def decorator_node(
    identifier=None,
    node_type="Normal",
    properties=None,
    inputs=None,
    outputs=None,
    catalog="Others",
    type="function",
):
    """Generate a decorator that register a function as a SciNode node.

    Attributes:
        indentifier (str): node identifier
        catalog (str): node catalog
        args (list): node args
        kwargs (dict): node kwargs
        properties (list): node properties
        inputs (list): node inputs
        outputs (list): node outputs
    """
    properties = properties or []
    inputs = inputs or []
    outputs = outputs or []

    def decorator(func):
        import cloudpickle as pickle
        from scinode.utils.decorator import generate_input_sockets, register_node

        nonlocal identifier

        if identifier is None:
            identifier = func.__name__
        # use cloudpickle to serialize function
        executor = {
            "executor": pickle.dumps(func),
            "type": type,
            "is_pickle": True,
        }
        #
        # Get the args and kwargs of the function
        args, kwargs, _inputs = generate_input_sockets(func, inputs, properties)
        # I don't know why isinstance(func.node_class, CalcFunctionNode) is False
        # print("func: ", func)
        # print("node_class: ", func.node_class)
        if func.node_class is CalcFunctionNode:
            node_type = "calcfunction"
        elif func.node_class is WorkFunctionNode:
            node_type = "workfunction"
        else:
            node_type = "Normal"
        node = register_node(
            identifier,
            node_type,
            args,
            kwargs,
            properties,
            _inputs,
            outputs,
            executor,
            catalog=catalog,
        )
        func.identifier = identifier
        func.node = node
        return func

    return decorator


class NodeDecoratorCollection:
    """Collection of node decorators."""

    node = staticmethod(decorator_node)

    __call__: Any = node  # Alias '@node' to '@node.node'.


node = NodeDecoratorCollection()

if __name__ == "__main__":
    from aiida.engine import calcfunction
    from aiida_worktree.decorator import node

    @node(
        identifier="MyAdd",
        outputs=[["General", "result"]],
        type="calcfunction",
    )
    @calcfunction
    def myadd(x, y):
        return x + y

    print(myadd.node)
