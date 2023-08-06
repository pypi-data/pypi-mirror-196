"""
Miscellaneous functions
"""

import sys
import traceback


def boolstr_to_bool(s):
    """
    Cast string that describes bool values ("False", "yes", "1", "0")
    into bool type.
    """
    t = s.lower().replace('false', '0').replace('true', '1').\
        replace('no', '0').replace('yes', '1')
    return bool(int(t))


def map_dict_deep(d, mapfunc):
    """
    Return a new dictionary whose keys are not changed, and the values (if they are not
    dictionaries) are passed through the map function. If the value is a (nested) dictionary,
    it undergoes the same processing.

    Args:
        d (dict): dictionary to process,
        mapfunc (function): map function of type (value) -> (value).
    """
    result = {}
    for k, v in d.items():
        if not isinstance(v, dict):
            v = mapfunc(v)
        else:
            v = map_dict_deep(v, mapfunc)
        result[k] = v
    return result


def map_deep(e, mapfunc, *, map_dict=True, map_list=True):
    """
    Same as map_dict_deep but also map the elements of lists.

    Args:
        e: element to process,
        mapfunc (function): map function of type (value) -> (value).
    """
    opts = (lambda **kw: kw)(map_dict=map_dict, map_list=map_list)
    if isinstance(e, dict) and map_dict:
        result = {k: map_deep(v, mapfunc, **opts) for k, v in e.items()}
    elif isinstance(e, list) and map_list:
        result = [map_deep(v, mapfunc, **opts) for v in e]
    else:
        result = mapfunc(e)
    return result


def format_exception(tb=False):
    """
    Formats exception message using sys.exc_info.
    Replaces newlines with spaces (only if tb==False)

    Args:
        tb (bool, optional): If True, prints traceback information. Defaults to False.
    """
    if tb:
        text = traceback.format_exc()
    else:
        exc_type, exc_value = sys.exc_info()[:2]
        text = '{}: {}'.format(exc_type.__name__, str(exc_value))
        text = text.replace('\n', ' ')
    return text
