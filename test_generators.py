import pytest
from generators import sanitize


def test_sanitize():
    d = {"abcx": 1, "ab": 1, "cd": 1, "y": 1, "d": 1}
    assert {"ab": 1, "cd": 1, "d": 1} == sanitize(d, "abcd")
