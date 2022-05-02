
from pygradethis.conditions import *
from pygradethis.python_grader import *

# Grade result -------------------------------------

def test_pass_if_correct():
    result = grade(
        python_pass_if(2, "Woah, nice!"),
        user_code="2", 
        solution_code="2", 
    )
    assert result['correct']
    assert result['type'] == "success"

def test_pass_if_incorrect():
    result = grade(
        python_pass_if(2, "Woah, nice!"),
        user_code="1", 
        solution_code="2", 
    )
    assert not result['correct']
    assert result['type'] == "error"

def test_multiple_pass_if_correct():
    result = grade(
        python_pass_if(2, "Woah, nice!"),
        python_pass_if(3, "Piece of cake!"),
        user_code="3",
    )
    assert result['correct']
    assert result['type'] == "success"

def test_multiple_pass_if_incorrect():
    result = grade(
        python_pass_if(2, "Woah, nice!"),
        python_pass_if(3, "Piece of cake!"),
        user_code="1",
    )
    assert not result['correct']
    assert result['type'] == "error"

def test_pass_if_fail_if_correct():
    result = grade(
        python_pass_if(2, "Noice!"),
        python_fail_if(1, "We do not want 1."),
        user_code="2",
        solution_code="2", 
    )
    assert result['correct']
    assert result['type'] == "success"

def test_pass_if_fail_if_incorrect():
    result = grade(
        python_pass_if(2, "Noice!"),
        python_fail_if(1, "We do not want 1."),
        user_code="1",
        solution_code="2", 
    )
    assert not result['correct']
    assert result['type'] == "error"

def test_fail_if_correct():
    # single fail_if; if user don't match any fail_ifs, count as correct by default
    result = grade(
        python_fail_if(1, "We wanted 1."),
        user_code="3",
    )
    assert result['correct']
    assert result['type'] == "success"

def test_fail_if_incorrect():
    result = grade(
        python_fail_if(1, "We wanted 1."),
        user_code="1",
    )
    assert not result['correct']
    assert result['type'] == "error"

def test_fail_ifs_correct():
    # multiple fail_ifs; if user don't match any fail_ifs, count as correct by default
    result = grade(
        python_fail_if(1, "We do not want 1."),
        python_fail_if(2, "We do not want 2."),
        user_code="3",
    )
    assert result['correct']
    assert result['type'] == "success"

def test_fail_ifs_incorrect():
    result = grade(
        python_fail_if(1, "We do not want 1."),
        python_fail_if(2, "We do not want 2."),
        user_code="2",
    )
    assert not result['correct']
    assert result['type'] == "error"

# Grade unittest style -------------------------------------
def test_unittest_style_correct():
    # TODO we now need a way to pass functions so we can test multiple
    # conditions :D 
    result = grade(
        python_pass_if(1),
        user_code="1",
        unittest_style=True
    )
    assert result['message'] == '1/1 correct.'
    assert result['num_correct'] == 1
    assert result['type'] == "success"

def test_unittest_style_incorrect():
    result = grade(
        python_pass_if(1),
        user_code="2",
        unittest_style=True
    )
    assert result['message'] == '0/1 correct.'
    assert result['num_correct'] == 0
    assert result['type'] == "error"

# Grade code -------------------------------------
# TODO add static code check examples
