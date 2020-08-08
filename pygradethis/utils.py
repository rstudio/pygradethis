"""
Module with useful functions.
"""

from typing import Union, List
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
