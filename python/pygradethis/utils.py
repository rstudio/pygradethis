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

def get_last_value(script: str, globals: dict) -> Any:
    """Evaluate Python code and return the value of the last Expression

    Parameters
    ----------
    script : str
        A string of Python code
    globals : dict
        A dictionary for the environment in which to evaluate code

    Returns
    -------
    Any
        A Python object
    """
    # grab list of AST nodes
    stmts = list(ast.iter_child_nodes(ast.parse(script)))
    # first execute entire source (since we need statements to be executed)
    exec(compile(script, filename="<string>", mode="exec"), globals)
    # then, execute last expression
    # TODO: we are assuming here that the last statement is an expression, we could
    # do the work to figure that out first and perhaps throw an error if there were no expressions
    return eval(compile(ast.Expression(body=stmts[-1].value), filename="<ast>", mode="eval"), globals)
