from pygradethis.grade_code import grade_code
from collections import namedtuple

# convenience tuple for structuring test cases
Case = namedtuple("Case", ["actual", "expected", "message"])

def test_primitives():
    test_cases = [
        # different literals
        Case(
            "\"1\"", "1",
            "I expected `1`, but what you wrote was interpreted as `\"1\"` at line 1."
        ),
        Case(
            "1", "\"1\"", 
            "I expected `\"1\"`, but what you wrote was interpreted as `1` at line 1."
        ),
        Case(
            "True", "\"1\"", 
            "I expected `\"1\"`, but what you wrote was interpreted as `True` at line 1."
        ),
        Case(
            "False", "\"1\"", 
            "I expected `\"1\"`, but what you wrote was interpreted as `False` at line 1."
        ),
        # str vs str
        Case(
            "\"not hello\"", "\"hello\"", 
            "I expected `\"hello\"`, but what you wrote was interpreted as `\"not hello\"` at line 1."
        ),
        # lists
        Case(
            "[1]", "\"1\"", 
            "I expected `\"1\"`, but what you wrote was interpreted as `[1]` at line 1."
        ),
        Case(
            "[2]", "[]", 
            "I did not expect `2` at line 1."
        ),
        Case(
            "[1,2]", "[1]", 
            "I did not expect `2` at line 1."
        ),
        Case(
            "[1]", "[1,2]", 
            "I expected `2` at line 1."
        ),
        # expr vs something else
        Case(
            "1 + 1", "1", 
            "I expected `1`, but what you wrote was interpreted as `1 + 1` at line 1."
        ),
        Case(
            "1 + (2 + 2)", "1 + (2 + 3)", 
            "I expected `3`, but what you wrote was interpreted as `2` at line 1."
        ),
        Case(
            "-1", "1", 
            "I expected `1`, but what you wrote was interpreted as `-1` at line 1."
        ),
    ]
    for t in test_cases:
        actual_message = grade_code(t.actual, t.expected)
        assert t.message == actual_message, (
            "Failed test case!\nUser:{}\nSolution:{}\nExpected:{}\nGot:{}".format(
                t.actual,
                t.expected,
                t.message,
                actual_message
            )
        )

def test_function_calls():
    test_cases = [
        Case(
            "2 + sum([1,2])", "2 + sum([1,1])", 
            "I expected `[1, 1]`, but what you wrote was interpreted as `[1, 2]` in `sum([1, 2])` at line 1."
        ),
        Case(
            "sqrt(log(2))", "sqrt(log(1))", 
            "I expected `log(1)`, but what you wrote was interpreted as `log(2)` in `sqrt(log(2))` at line 1."
        ),
        Case(
            "def foo(a, b=1): pass; foo(2)", "def foo(a, b=1): pass; foo(1)", 
            "I expected `1`, but what you wrote was interpreted as `2` in `foo(2)` at line 1."
        ),
        Case(
            "def foo(a, b=1): pass; foo(a=2)", "def foo(a, b=1): pass; foo(1)", 
            "I expected `1`, but what you wrote was interpreted as `2` in `foo(a=2)` at line 1."
        ),
        Case(
            "def foo(a, b=1): pass; foo(a=[2])", "def foo(a, b=1): pass; foo(2, 2)", 
            "I expected `2`, but what you wrote was interpreted as `[2]` in `foo(a=[2])` at line 1."
        ),
        Case(
            "def foo(a, b=1): pass; foo(a=\"2\", b=2)", "def foo(a, b=1): pass; foo(2, 2)", 
            "I expected `2`, but what you wrote was interpreted as `\"2\"` in `foo(a=\"2\", b=2)` at line 1."
        ),
        Case(
            "def head(n=5): pass; head(12)", "def head(n=5): pass; head(n=10)", 
            "I expected `10`, but what you wrote was interpreted as `12` in `head(12)` at line 1."
        ),
    ]
    for t in test_cases:
        actual_message = grade_code(t.actual, t.expected)
        assert t.message == actual_message, (
            "Failed test case!\nUser:{}\nSolution:{}\nExpected:{}\nGot:{}".format(
                t.actual,
                t.expected,
                t.message,
                actual_message
            )
        )

