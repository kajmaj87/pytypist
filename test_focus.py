import pytest

from focus import focus, probabilities, calculate_main_focus, calculate_secondary_focus


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


def test_calculate_secondary_focus():
    assert "xyz" == calculate_secondary_focus("yyyyaabcxxxxxzzz")


def test_calculate_secondary_focus_less_than_amount():
    assert "x" == calculate_secondary_focus("xxxx", amount=2)


def test_calculate_secondary_focus_less_than_threshold():
    assert "xz" == calculate_secondary_focus("xxxxzzabc", threshold=2)


def test_probabilities_simple():
    d = {"a": 1}
    assert {"a": 1} == probabilities(d)


def test_probabilities_simple_with_frequency():
    d = {"a": 5}
    assert {"a": 1} == probabilities(d)


def test_probabilities():
    d = {"a": 1, "b": 2, "acccb": 1}
    assert {"a": 0.5, "b": 0.75, "c": 0.25} == probabilities(d)
