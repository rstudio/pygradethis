"""
This module holds functions for common mistakes and generating messages for
feedback to the student.
"""

import ast
from typing import Dict, Any
from .formatters import formatted

def missing(left: Any, right: Any, line_info: Dict[str, int]):
    """Generates message when user is missing a node or element in code.

    Parameters
    ----------
    left : Any
        an ast.Node, a custom type, or a python data type
    right : Any
        an ast.Node, a custom type, or a python data type
    line_info : Dict[str, int]
        holds line information about a particular node
    """
    msg = "I expected {} at line {}."
    msg_args = (
        formatted(right), 
        line_info.get("left")
    )
    assert type(left) == type(right), msg.format(*msg_args)

def not_expected(left: Any, right: Any, line_info: Dict[str, int]):
    """Generates message when user supplies an extra node or element in code.

    Parameters
    ----------
    left : Any
        an ast.Node, a custom type, or a python data type
    right : Any
        an ast.Node, a custom type, or a python data type
    line_info : Dict[str, int]
        holds line information about a particular node
    """
    msg = "I did not expect {} at line {}."
    msg_args = (
        formatted(left), 
        line_info.get("left")
    )
    assert type(left) == type(right), msg.format(*msg_args)

def wrong_value(left: Any, right: Any, line_info: Dict[str, int],last_parent: str, condition: bool):
    """Generates message when user's code contains in an incorrect value.

    Parameters
    ----------
    left : Any
        an ast.Node, a custom type, or a python data type
    right : Any
        an ast.Node, a custom type, or a python data type
    line_info : Dict[str, int]
        holds line information about a particular node
    last_parent : str
        the nearest parent that can be converted to source text
    condition : bool
        the condition we want to check regarding equality between left and right
        ast nodes or values
    """
    msg = "I expected {}, but what you wrote was interpreted as {} at line {}."
    msg_args = (
        formatted(right),
        formatted(left),
        line_info.get("left"),
    )
    if (formatted(left) != last_parent 
        and not isinstance(left, ast.AST)
        and not isinstance(left, ast.Call)):
        msg = "I expected {}, but what you wrote was interpreted as {} in {} at line {}."
        msg_args = (
            formatted(right),
            formatted(left),
            last_parent,
            line_info.get("left"),
        )
    assert condition, msg.format(*msg_args)

# Call related -------------------------------

def missing_argument(left_call, right_call, right_source, e):
    # def foo(a, b=1): pass
    # foo() missing 1 required positional argument: 'a'

    # "Your call to {this} should include {that_name} ",
    # "You may have misspelled an argument name, ",
    # "or left out an important argument."
    msg = "I expected {} but what you wrote was interpreted as {}, which I can't execute because I'm {}."
    msg_args = (
        right_source, 
        formatted(left_call), 
        str(e).lower()
    )
    raise AssertionError(msg.format(*msg_args))

def unexpected_argument(left_call, right_call, right_source, e):
    # def foo(a, b=1): pass
    # foo(x=1)

    # TypeError: foo() got an unexpected keyword argument 'x'

    # {this} got an unexpected keyword argument {this_name}
    msg = "I expected {} but what you wrote was interpreted as {}, which I can't execute because I {}."
    msg_args = (
        right_source, 
        formatted(left_call), 
        str(e).lower()
    )
    raise AssertionError(msg.format(*msg_args))


def repeated_argument(e):
    # def foo(a, b=1): pass

    # foo(a=1, a=2)
    # SyntaxError: keyword argument repeated

    # "You passed multiple arguments named {this_name} to {this_call}, which will cause "
    # "an error. Check your spelling, or remove one of the arguments."
    return "You passed a keyword argument multiple times."

def wrong_call(this, that):
    # def foo(a, b=1): pass

    # bar(1)
    # foo(1)

    # "I expected you to call {that} where you called {this}."
    pass



def surplus_argument(this, this_arg):

    # def foo(a, b=1): pass
    # foo(x=1) => TypeError: foo() got an unexpected keyword argument 'x'

    # "I did not expect your call to {this} to ",
    # "include {this_arg}. You ",
    # "may have included an unnecessary argument, or you ",
    # "may have left out or misspelled an important ",
    # "argument name."
    pass
