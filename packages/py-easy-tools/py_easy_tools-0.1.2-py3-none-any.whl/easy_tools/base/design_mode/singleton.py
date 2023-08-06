from functools import wraps


def singleton(cls):
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return get_instance


def singleton_unique(cls):
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kw):
        unique_key = "{}_{}_{}".format(cls, args, kw)
        if unique_key not in instances:
            instances[unique_key] = cls(*args, **kw)
        return instances[unique_key]

    return get_instance
