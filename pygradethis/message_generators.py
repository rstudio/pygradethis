"""
This module holds functions for common mistakes and generating messages for
feedback to the student.
"""

import ast
from typing import Dict, Any
from .formatters import formatted

def missing(left: Any, right: Any, line_info: Dict[str, int]) -> None:
    """Generates message when user is missing a node or element in code.

    Parameters
    ----------
    left : Any
        an ast.Node, a custom type, or a python data type
    right : Any
        an ast.Node, a custom type, or a python data type
    line_info : Dict[str, int]
        holds line information about a particular node

    Returns
    -------
    str
        feedback message
    """
    msg = "I expected `{}` at line {}."
    msg_args = (
        formatted(right), 
        line_info.get("left")
    )
    assert type(left) == type(right), msg.format(*msg_args)

def not_expected(left: Any, right: Any, line_info: Dict[str, int]) -> None:
    """Generates message when user supplies an extra node or element in code.

    Parameters
    ----------
    left : Any
        an ast.Node, a custom type, or a python data type
    right : Any
        an ast.Node, a custom type, or a python data type
    line_info : Dict[str, int]
        holds line information about a particular node

    Returns
    -------
    str
        feedback message
    """
    msg = "I did not expect `{}` at line {}."
    msg_args = (
        formatted(left), 
        line_info.get("left")
    )
    assert type(left) == type(right), msg.format(*msg_args)

def wrong_value(left: Any, right: Any, line_info: Dict[str, int], condition: bool, last_parent: str) -> None:
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
    
    Returns
    -------
    str
        feedback message
    """
    msg = "I expected `{}`, but what you wrote was interpreted as `{}` at line {}."
    msg_args = (
        formatted(right),
        formatted(left),
        line_info.get("left"),
    )
    if last_parent != "" and last_parent != formatted(left):
        msg = "I expected `{}`, but what you wrote was interpreted as `{}` in `{}` at line {}."
        msg_args = (
            formatted(right),
            formatted(left),
            last_parent,
            line_info.get("left")
        )
    assert condition, msg.format(*msg_args)

# Call related -------------------------------

def repeated_argument(e: SyntaxError) -> str:
    """Generates a feedback for a repeated keyword argument error.

    Parameters
    ----------
    e : SyntaxError
        the error object

    Returns
    -------
    str
        feedback message
    """
    msg = "I couldn't parse your function call because I got a repeated keyword argument."
    return msg.format(str(e).lower())

def missing_argument(left_call: ast.AST, right_source: str, e: str) -> None:
    """Generates a feedback when there is a missing argument for a function call.

    Parameters
    ----------
    left_call : ast.AST
        student's function call
    right_source : str
        solution source text
    e : TypeError
        the error object

    Raises
    ------
    AssertionError
        to ripple up back to grade_code
    """
    msg = "I expected `{}` but what you wrote was interpreted as `{}`, which I can't execute because I'm {}."
    msg_args = (
        right_source, 
        formatted(left_call), 
        str(e).lower()
    )
    raise AssertionError(msg.format(*msg_args))

def unexpected_argument(left_call: ast.AST, right_source: str, e: str) -> None:
    """Generates a feedback when there is an unexpected argument for a function call.

    Parameters
    ----------
    left_call : ast.AST
        student's function call
    right_source : str
        solution source text
    e : TypeError
        the error object
    
    Raises
    ------
    AssertionError
        to ripple up back to grade_code
    """
    msg = "I expected `{}` but what you wrote was interpreted as `{}`, which I can't execute because I {}."
    msg_args = (
        right_source, 
        formatted(left_call), 
        str(e).lower()
    )
    raise AssertionError(msg.format(*msg_args))

def surplus_argument(left_call: ast.AST, right_source: str, e: str) -> None:
    """Generates a feedback when there extra arguments for a function call.

    Parameters
    ----------
    left_call : ast.AST
        student's function call
    right_source : str
        solution source text
    e : TypeError
        the error object
        
    Raises
    ------
    AssertionError
        to ripple up back to grade_code
    """
    msg = "I expected `{}` but what you wrote was interpreted as `{}`, which I can't execute because there are `{}`."
    msg_args = (
        right_source, 
        formatted(left_call), 
        str(e).lower()
    )
    raise AssertionError(msg.format(*msg_args))
