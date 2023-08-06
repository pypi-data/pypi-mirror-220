import scinode
import aiida


class WorkTree(scinode.core.nodetree.NodeTree):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def run(self):
        from aiida_worktree.engine.worktree import WorkTree

        ntdata = self.to_dict()
        all = {"nt": ntdata}
        _result, self.process = aiida.engine.run_get_node(WorkTree, **all)
        # self.process.base.extras.set("worktree", ntdata)
        self.update()

    def submit(self, wait=False, timeout=60):
        from aiida_worktree.engine.worktree import WorkTree
        from aiida_worktree.utils import merge_properties

        ntdata = self.to_dict()
        # merge the kwargs
        merge_properties(ntdata)
        all = {"nt": ntdata}
        # print("ntdata: ", ntdata)
        self.process = aiida.engine.submit(WorkTree, **all)
        # self.process.base.extras.set("worktree", ntdata)
        if wait:
            self.wait(timeout=timeout)

    def wait(self, timeout=50):
        """Wait for worktree to finish."""
        import time

        start = time.time()
        self.update()
        while self.state not in (
            "PAUSED",
            "FINISHED",
            "FAILED",
            "CANCELLED",
            "EXCEPTED",
        ):
            time.sleep(0.5)
            self.update()
            if time.time() - start > timeout:
                return

    def update(self):
        self.state = self.process.process_state.value.upper()
        self.pk = self.process.pk
        outgoing = self.process.base.links.get_outgoing()
        for link in outgoing.all():
            # I don't know why the process_state could be a 'NoneType' object
            node = link.node
            # print("label: ", link.link_label)
            if isinstance(node, aiida.orm.ProcessNode) and getattr(
                node, "process_state", False
            ):
                self.nodes[link.link_label].state = node.process_state.value.upper()
                self.nodes[link.link_label].node = node
                self.nodes[link.link_label].state = "FINISHED"
                self.nodes[link.link_label].pk = node.pk
            elif isinstance(node, aiida.orm.Data):
                label = link.link_label[9:]
                if label in self.nodes.keys():
                    self.nodes[label].state = "FINISHED"
                    self.nodes[label].node = node
                self.nodes[label].pk = node.pk
        # for normal python function
