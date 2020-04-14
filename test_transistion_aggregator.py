import pytest
from statistics import mean
from key_logger import Transition
from transition_aggregator import KeyStat


@pytest.fixture
def ta():
    from transition_aggregator import TransitionAggregator

    return TransitionAggregator()


def test_stages(ta):
    one_stage = [t("START")]
    two_stages = [t("START"), t("START")]

    assert ta.stages(one_stage) == 1
    assert ta.stages(two_stages) == 2


def test_error(ta):
    state_test_helper(ta, "ERROR", ta.errors)


def test_correct(ta):
    state_test_helper(ta, "CORRECT", ta.correct)


def test_erase(ta):
    state_test_helper(ta, "ERASE", ta.erases)


def state_test_helper(ta, state, fun):
    one = [t(st=state)]
    two = [t(st=state), t(st="OTHER"), t(st=state)]

    assert fun(one) == 1
    assert fun(two) == 2


def test_key_stats(ta):
    stage = [t(e="a", t=50), t(e="x", t=20), t(e="x", t=10), t(e="a", t=100)]

    assert {"a": [50, 100], "x": [20, 10]}.items() == ta.key_stats(stage).items()


def test_key_stats_should_not_count_first_char_in_stage(ta):
    stage = [
        t("START", e="s", t=0),
        t(e="a", t=50),
        t(e="x", t=20),
        t(e="x", t=10),
        t(e="a", t=100),
    ]

    assert {"a": [50, 100], "x": [20, 10]}.items() == ta.key_stats(stage).items()


def test_calculate_stats(ta):
    stats = {"a": [50, 100], "x": [20, 10]}
    assert {"a": 75, "x": 15}.items() == ta.calculate_stats(stats, mean).items()
    assert {"a": 100, "x": 20}.items() == ta.calculate_stats(stats, max).items()


def t(s="", e="", st="", t=0):
    return Transition(s, e, st, t)
