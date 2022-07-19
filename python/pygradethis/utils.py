"""
Module with useful functions.
"""

from typing import Union, List, Any
import ast

def parse_code(input: Union[str, List[str]]) -> str:
    """Tries to parse code represented as string or list of strings

    Parameters
    ----------
    input : Union[str, List[str]]
        either a str or a list of str

    Returns
    -------
    str
        the formatted string

    Raises
    ------
    SyntaxError
        if there are any parsing issues
    """
    if input is None:
        return input
    try:
        simple = "".join(input)
        ast.parse(simple)
        return simple
    except SyntaxError as e:
        if "EOF" in str(e):
            return "\n".join(input)
        else:
            raise SyntaxError("Problem parsing your code!")

def get_last_value(script: str, globals: dict = globals()) -> Any:
    """Evaluate Python code and return the value of the last line of code.

    Parameters
    ----------
    script : str
        A string of Python code
    globals : dict, optional
        A dictionary for the environment in which to evaluate code, by default globals()

    Returns
    -------
    Any
        A Python object, or None if the last line is not an expression

    Examples
    --------
    >>> get_last_value("x = 2; x + 1")
    3

    >>> get_last_value("2 + 2; x = 2") # returns None
    """
    stmts = list(ast.iter_child_nodes(ast.parse(script)))
    # iteratively walk through AST and execute statements and expressions while storing the last value
    last_value = None
    for s in stmts:
        if isinstance(s, ast.Expr):
            result = eval(compile(ast.Expression(body=s.value), filename="<ast>", mode="eval"), globals)
            last_value = result
        else:
            exec(compile(ast.Module(body=[s], type_ignores=[]), filename="<ast>", mode="exec"), globals)
            last_value = None
    return last_value
