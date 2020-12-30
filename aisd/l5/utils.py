
def is_iterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    return True


def has_label(obj):
    try:
        return obj.label
    except AttributeError:
        return False


def are_labeled(objs):
    return all(is_iterable(obj) and has_label(obj) for obj in objs)