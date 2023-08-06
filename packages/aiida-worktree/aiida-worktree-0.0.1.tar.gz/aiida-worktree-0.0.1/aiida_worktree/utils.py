def get_executor(data):
    """Import executor from path and return the executor and type."""
    import importlib
    from aiida.plugins import CalculationFactory, WorkflowFactory, DataFactory

    is_pickle = data.get("is_pickle", False)
    type = data.get("type", "function")
    if is_pickle:
        import cloudpickle as pickle

        executor = pickle.loads(data["executor"])
    else:
        if type == "WorkflowFactory":
            executor = WorkflowFactory(data["name"])
        elif type == "CalculationFactory":
            executor = CalculationFactory(data["name"])
        elif type == "DataFactory":
            executor = DataFactory(data["name"])
        else:
            module = importlib.import_module("{}".format(data.get("path", "")))
            executor = getattr(module, data["name"])

    return executor, type


def create_data_node(executor, args, kwargs):
    from aiida import orm

    # print("Create data node: ", executor, args, kwargs)
    extras = kwargs.pop("extras", {})
    repository_metadata = kwargs.pop("repository_metadata", {})
    if issubclass(executor, (orm.BaseType, orm.Dict)):
        data_node = executor(*args)
    else:
        data_node = executor(*args)
        data_node.base.attributes.set_many(kwargs)
    data_node.base.extras.set_many(extras)
    data_node.base.repository.repository_metadata = repository_metadata
    data_node.store()
    return data_node


def update_nested_dict(d, key, value):
    """
    d = {"base": {"pw": {"parameters": 1}}
    key = "base.pw.parameters"
    value = 2
    """
    keys = key.split(".")
    current = d
    for k in keys[:-1]:
        current = current.setdefault(k, {})
    current[keys[-1]] = value


def update_nested_dict_with_special_keys(d):
    # first remove None and empty value
    d = {k: v for k, v in d.items() if v is not None and v != {}}
    #
    special_keys = [k for k in d.keys() if "." in k]
    for key in special_keys:
        value = d.pop(key)
        update_nested_dict(d, key, value)
    return d


def merge_properties(ntdata):
    """Merge properties."""
    for name, node in ntdata["nodes"].items():
        for key, prop in node["properties"].items():
            if "." in key and prop["value"] not in [None, {}]:
                root, key = key.split(".", 1)
                update_nested_dict(
                    node["properties"][root]["value"], key, prop["value"]
                )
                prop["value"] = None


if __name__ == "__main__":
    d = {
        "base": {
            "pw": {"code": 1, "parameters": 1, "pseudos": 1, "metadata": 1},
            "kpoints": 1,
        },
        "base.pw.parameters": 2,
    }
    d = update_nested_dict_with_special_keys(d)
    print(d)
