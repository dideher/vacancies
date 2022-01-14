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
