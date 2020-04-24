import pytest

from focus import focus, weights, calculate_secondary_focus


def test_main_focus():
    d = {"a": 1, "b": 2, "c": 3}
    assert {"a": 1, "c": 3} == focus(d, "ac")


def test_secondary_focus():
    d = {"a": 1, "b": 2, "c": 3}
    # focus bumps the weight to the max found
    assert {"a": 3, "b": 2, "c": 3} == focus(d, secondary="ac")


def test_secondary_focus_should_add_bonuses():
    d = {"auto": 1, "ada": 1, "class": 1}
    # a is in 3 words, so has weight 3
    # c is in 1 word so has weight 1
    # c occurs 3 times less likely so its relative weight will be 3
    # this will be applied as gain each time c occurs in word, 1 will be applied for a as it is our max
    # weight will be added once for each corresponding letter in word
    assert {"auto": 1, "ada": 1 + 1, "class": 3 + 1} == focus(d, secondary="ac")


def test_both_focuses():
    d = {"alexa": 1, "benny": 2, "cleve": 3}
    # c has weight 3 as it occures once in cleve (which occures 3 times in dictionary)
    # both e and l have weight 4 (3 times in cleve, once in alexa)
    # c has relative wieght of 4/3, so we muliply current weight of each word with c by this ratio
    assert {"alexa": 1, "cleve": 4} == focus(d, main="ac", secondary="c")


def test_calculate_secondary_focus():
    # gives back letters according to their frequency (least seen first)
    assert "azy" == calculate_secondary_focus(
        {"x": [1, 2, 3, 4], "y": [1, 2, 3], "z": [1, 2], "a": [1]}, limit=3
    )


def test_weights_simle():
    d = {"a": 1}
    assert {"a": 1} == weights(d)


def test_weights_simple_with_frequency():
    d = {"a": 5}
    assert {"a": 5} == weights(d)


def test_weights():
    # these are word occurences
    d = {"a": 1, "b": 2, "acccb": 1}
    # this says in how many words this letter occur
    assert {"a": 2, "b": 3, "c": 1} == weights(d)
