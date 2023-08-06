"""
Tests for 'misc' module
"""

import json

from kevbits.misc import map_dict_deep, map_deep, format_exception


# pylint: disable=missing-docstring


def test_map_dict_deep():
    dinp = {'1': 1, 'a': 'A', 'd': {'3': 3, 'b': 'B', 'dd': {'5':  5, 'c': 'C'}}}
    dexp = {'1': 1, 'a': 'a', 'd': {'3': 3, 'b': 'b', 'dd': {'5':  5, 'c': 'c'}}}
    def mapfunc(v):
        return v if not isinstance(v, str) else v.lower()
    dout = map_dict_deep(dinp, mapfunc)
    assert json.dumps(dout, sort_keys=True) == json.dumps(dexp, sort_keys=True)


def test_map_deep():
    dinp = {'1': 1, 'a': 'A', 'd': {'3': 3, 'b': [{'5':  5, 'c': 'C'}]}}
    dexp = {'1': 1, 'a': 'a', 'd': {'3': 3, 'b': [{'5':  5, 'c': 'c'}]}}
    def mapfunc(v):
        return v if not isinstance(v, str) else v.lower()
    dout = map_deep(dinp, mapfunc)
    assert json.dumps(dout, sort_keys=True) == json.dumps(dexp, sort_keys=True)


#------------------------------------------------------------------------------
# format_exception() tests
#------------------------------------------------------------------------------

def func1():
    return tuple()[1]   # IndexError

def excgen():
    return func1()

def get_format_exception(tb=False):
    try:
        excgen()
    except Exception:
        return format_exception(tb)


def test_format_exception():
    assert get_format_exception() == 'IndexError: tuple index out of range'


expected = '''Traceback (most recent call last):
  File "<path-to-this-file>", line 14, in get_format_exception
    excgen()
  File "<path-to-this-file>", line 10, in excgen
    return func1()
  File "<path-to-this-file>", line 7, in func1
    return tuple()[1]   # IndexError
'''.splitlines()

def test_format_exception_tb():
    lines = get_format_exception(tb=True).splitlines()
    assert lines[0] == "Traceback (most recent call last):"
    lines.index("    return tuple()[1]   # IndexError")  # expect no exception
