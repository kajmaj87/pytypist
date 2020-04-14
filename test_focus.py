import pytest

from focus import focus


def test_main_focus():
    d = {"a": 1, "b": 2, "c": 3}
    assert {"a": 1, "c": 3} == focus(d, "ac")


def test_secondary_focus():
    d = {"a": 1, "b": 2, "c": 3}
    assert {"a": 5, "b": 2, "c": 15} == focus(d, secondary="ac", gain=5)


def test_secondary_focus_should_add_bonuses():
    d = {"auto": 1, "ada": 1, "class": 1}
    assert {"auto": 5, "ada": 5, "class": 10} == focus(d, secondary="ac", gain=5)


def test_both_focuses():
    d = {"alex": 1, "benny": 2, "cleve": 3}
    assert {"alex": 1, "cleve": 15} == focus(d, main="ac", secondary="c", gain=5)
