from functools import wraps

def is_empty(object):
    """
    Returns `True` if the object is empty (ie Null or equal to an empty string)
    :param object:
    :return:
    """
    if object is None:
        return True
    else:
        return str(object).strip() == ''


def disable_for_loaddata(signal_handler):
    """
    Decorator that turns off signal handlers when loading fixture data.
    """
    # inspired from https://stackoverflow.com/questions/15624817/have-loaddata-ignore-or-disable-post-save-signals
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs.get('raw'):
            return
        signal_handler(*args, **kwargs)
    return wrapper
