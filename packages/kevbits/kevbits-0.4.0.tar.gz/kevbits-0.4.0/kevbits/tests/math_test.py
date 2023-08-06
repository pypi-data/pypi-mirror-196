"""
Tests for 'angles' module
"""

from kevbits.math import closest_mod


# pylint: disable=missing-docstring


def test_closest_mod():
    assert closest_mod(0., 0., 1.) == 0.
    assert closest_mod(1., 1., 1.) == 1.
    assert closest_mod(-1., -1., 1.) == -1.

    assert closest_mod(0., 3.49, 1.) == 3.0
    assert closest_mod(0., 3.51, 1.) == 4.0

    assert closest_mod(0., -3.49, 1.) == -3.0
    assert closest_mod(0., -3.51, 1.) == -4.0
