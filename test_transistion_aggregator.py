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


def test_error_simple(ta):
    stage = prepare_stage("abcd", "ac<bcx<d")
    assert ta.errors(stage) == 2


def test_error_multiple_consecutive(ta):
    stage = prepare_stage("abcd", "acbd<<<bcx<d")
    assert ta.errors(stage) == 2


def test_adjusted_keys_should_not_count_first_element(ta):
    stage_with_correct = [
        t(s="START", e="s", st="CORRECT", t=0),
    ]
    stage_with_error = [
        t(s="START", e="s", st="ERROR", t=0),
    ]

    assert {}.items() == ta.adjusted_key_stats(stage_with_error).items()
    assert {}.items() == ta.adjusted_key_stats(stage_with_correct).items()


def test_adjusted_keys_should_not_count_first_error(ta):
    stage = [
        t(s="START", e="s", st="ERROR", t=0),
        t(e="a", st="ERROR", t=50),
        t(e="x", st="ERASE", t=20),
        t(e="x", st="ERASE", t=10),
        t(e="a", st="CORRECT", t=100),
        t(e="a", st="CORRECT", t=50),
        t(e="x", st="CORRECT", t=50),
    ]
    assert {"a": [180, 50], "x": [50]}.items() == ta.adjusted_key_stats(stage).items()


def test_last_real_errors(ta):
    stage = prepare_stage("ax", "ab<x")
    assert "x" == ta.last_errors(stage)


def test_last_real_errors_big(ta):
    stage = prepare_stage("abccc", "axyz<<<bx<cxx<d<<cc")
    assert "bcc" == ta.last_errors(stage)


def test_last_real_errors_big_with_limit(ta):
    stage = prepare_stage("abccc", "axyz<<<bx<cxx<d<<cc")
    assert "bc" == ta.last_errors(stage, max_errors=2)


def test_last_real_errors_with_consecutive_corrections_and_typo_on_correct(ta):
    stage = prepare_stage("abcd", "acbd<<<bcx<d")
    assert "bd" == ta.last_errors(stage)


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


def test_time_spent_on_errors(ta):
    stages = prepare_stage("abc", "ac<bd<c", key_time=100)
    assert 0.4 == ta.time_fixing_errors(stages)


def test_total_time_spent(ta):
    stages = prepare_stage("abc", "ac<bd<c", key_time=100)
    assert 0.7 == ta.total_time(stages)


def test_time_if_without_errors(ta):
    stages = prepare_stage("abc", "ac<bd<c", key_time=100)
    assert 0.3 == round(ta.time_if_without_errors(stages), 1)


def test_prepare_stage_onechar():
    stages = prepare_stage("a", "a")
    assert stages == [t(s="START", e="a", st="CORRECT", t=10)]


def test_prepare_stage_with_correction_simple():
    stages = prepare_stage("ax", "ab<x")
    assert stages == [
        t(s="START", e="a", st="CORRECT", t=10),
        t(s="a", e="b", st="ERROR", t=10),
        t(s="b", e="ERASE", st="ERASE", t=10),
        t(s="ERASE", e="x", st="CORRECT", t=10),
    ]


def test_prepare_stage_with_two_typos_should_not_mark_second_as_correct():
    stages = prepare_stage("abc", "acb")
    assert stages == [
        t(s="START", e="a", st="CORRECT", t=10),
        t(s="a", e="c", st="ERROR", t=10),
        t(s="c", e="b", st="ERROR", t=10),
    ]


def test_prepare_stage_with_correction():
    stages = prepare_stage("abc", "ac<bc")
    assert stages == [
        t(s="START", e="a", st="CORRECT", t=10),
        t(s="a", e="c", st="ERROR", t=10),
        t(s="c", e="ERASE", st="ERASE", t=10),
        t(s="ERASE", e="b", st="CORRECT", t=10),
        t(s="b", e="c", st="CORRECT", t=10),
    ]


def test_prepare_stage_with_consecutive_typos_one_of_them_on_correct_place():
    stages = prepare_stage("abc", "acc<<bc")
    assert stages == [
        t(s="START", e="a", st="CORRECT", t=10),
        t(s="a", e="c", st="ERROR", t=10),
        t(s="c", e="c", st="ERROR", t=10),
        t(s="c", e="ERASE", st="ERASE", t=10),
        t(s="ERASE", e="ERASE", st="ERASE", t=10),
        t(s="ERASE", e="b", st="CORRECT", t=10),
        t(s="b", e="c", st="CORRECT", t=10),
    ]


def prepare_stage(stage_text, written_text, delete_char="<", key_time=10):
    first_key = True
    result = []
    char_in_text = 1
    check_chars = (
        lambda x, y: "CORRECT" if x == y else "ERASE" if l == delete_char else "ERROR"
    )
    transform_erase = lambda x: "ERASE" if x == delete_char else x
    last_key = "START"
    current_text = ""
    for l in written_text:
        if l == delete_char:
            current_text = current_text[:-1]
            state = "ERASE"
        else:
            current_text += l
            if current_text == stage_text[:char_in_text]:
                state = "CORRECT"
                char_in_text += 1
            else:
                state = "ERROR"
        result.append(
            t(s=transform_erase(last_key), e=transform_erase(l), st=state, t=key_time)
        )
        last_key = l

    # state = check_chars(l, stage_text[char_in_text])
    # result.append(
    #     t(s=transform_erase(last_key), e=transform_erase(l), st=state, t=key_time,)
    # )
    # last_key = l
    # char_in_text += 1 if state == "CORRECT" else 0

    return result


def t(s="", e="", st="", t=0):
    return Transition(s, e, st, t)
