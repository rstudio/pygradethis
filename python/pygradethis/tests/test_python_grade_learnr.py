from re import U
from pygradethis.conditions import *
from pygradethis.pygradethis_exercise_checker import *

# Grade result -------------------------------------

def test_pass_if_correct():
    check_code = """grade_result(
        pass_if_equals(2, "Woah, nice!"),
        user_result = last_value
    )"""
    result = pygradethis_exercise_checker(
        user_code="2",
        solution_code="2",
        check_code=check_code,
        last_value = 2
    )
    assert result['correct']
    assert result['type'] == "success"
    assert "Woah, nice!" in result['message']


def test_pass_if_incorrect():
    check_code = """grade_result(
        pass_if_equals(2, "Woah, nice!"),
        user_result = last_value
    )"""
    result = pygradethis_exercise_checker(
        user_code="1",
        solution_code="2",
        check_code=check_code,
        last_value = 1
    )
    assert not result['correct']
    assert result['type'] == "error"
    assert result['message'] != ""


def test_multiple_pass_if_correct():
    check_code = """grade_result(
        pass_if_equals(2, "Woah, nice!"),
        pass_if_equals(3, "Piece of cake!"),
        user_result = last_value
    )"""
    result = pygradethis_exercise_checker(
        user_code="3",
        solution_code="2",
        check_code=check_code,
        last_value = 3
    )
    assert result['correct']
    assert result['type'] == "success"
    assert "Piece of cake!" in result['message']

    # a different correct value
    check_code = """grade_result(
        pass_if_equals(2, "Woah, nice!"),
        pass_if_equals(3, "Piece of cake!"),
        user_result = last_value
    )"""
    result = pygradethis_exercise_checker(
        user_code="2",
        solution_code="2",
        check_code=check_code,
        last_value = 2
    )
    assert result['correct']
    assert result['type'] == "success"
    assert "Woah, nice!" in result['message']

def test_multiple_pass_if_incorrect():
    check_code = """grade_result(
        pass_if_equals(2, "Woah, nice!"),
        pass_if_equals(3, "Piece of cake!"),
        user_result = last_value
    )"""
    result = pygradethis_exercise_checker(
        user_code="3",
        solution_code="2",
        check_code=check_code,
        last_value = 1
    )
    assert not result['correct']
    assert result['type'] == "error"
    assert result['message'] != ""

def test_pass_if_fail_if_correct():
    check_code = """grade_result(
        pass_if_equals(2, "Nice work!"),
        fail_if_equals(1, "We do not want 1."),
        user_result = last_value
    )"""
    result = pygradethis_exercise_checker(
        user_code="2",
        solution_code="2",
        check_code=check_code,
        last_value = 2
    )
    assert result['correct']
    assert result['type'] == "success"
    assert "Nice work!" in result['message']

def test_pass_if_fail_if_incorrect():
    check_code = """grade_result(
        pass_if_equals(2, "Nice work!!"),
        fail_if_equals(1, "We do not want 1."),
        user_result = last_value
    )"""
    result = pygradethis_exercise_checker(
        user_code="1",
        solution_code="2",
        check_code=check_code,
        last_value = 1
    )
    assert not result['correct']
    assert result['type'] == "error"
    assert "We do not want 1." in result['message']
