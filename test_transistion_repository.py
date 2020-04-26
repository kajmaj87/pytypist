import pytest
from transition_repository import limit
from util_tests import prepare_stage, t
from util import flatten


def test_should_not_limit_when_too_high():
    stage = prepare_stage("aaa", "aaa")
    assert stage == limit(stage, 3)


def test_that_correct_start_char_is_not_counted_towards_the_limit():
    stages = flatten([prepare_stage("aa", "aa"), prepare_stage("aa", "aa")])
    assert stages == limit(stages, 3)


def test_should_limit_to_max_correct_chars():
    stage = prepare_stage("aaa", "aaa", key_time=0)
    assert [t("a", "a", "CORRECT"), t("a", "a", "CORRECT")] == limit(stage, 2)


def test_should_limit_to_max_correct_chars_also_taking_errors():
    stage = prepare_stage("aaaa", "aab<aa", key_time=0)
    assert [
        t("a", "b", "ERROR"),
        t("b", "ERASE", "ERASE"),
        t("ERASE", "a", "CORRECT"),
        t("a", "a", "CORRECT"),
    ] == limit(stage, 2)
