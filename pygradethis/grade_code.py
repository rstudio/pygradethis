"""
This module is used to check if a user's code is equal to solution code and
note when the two differ.
"""

# parsing
import parser
import ast
import astunparse

# formatting
from .formatters import formatted
# checking functions
from .check_functions import standardize_arguments
# feedback
from .message_generators import missing, not_expected, wrong_value

# add any libraries you might need
from math import *

# misc
from itertools import zip_longest
from typing import Optional, Dict, Any

def new_parent_source(tree: Any, last_parent: str) -> str:
    """Given an ast, the current tree, and the last parent source,
    return a new last parent source for facilitating feedback on problematic
    node.

    Parameters
    ----------
    tree : Any
        the node we want to extract the source text for
    last_parent : str
        the nearest parent that can be converted to source text

    Returns
    -------
    str
        the new last_parent or the same
    """
    # attempt to get a new parent source text for feedback
    try:
        parent_source = formatted(tree)
    except:
        pass
    # only set the last_parent if:
    # - it is a compound ast, and
    # - we can get a source text
    if isinstance(tree, ast.AST) and len(tree._fields) > 1 and parent_source != "":
        last_parent = parent_source
    return last_parent

def check_children(left: ast.AST, 
                   right: ast.AST, 
                   line_info: Optional[Dict[str, int]] = None,
                   last_parent: str = "",
                   left_source: str = "", 
                   right_source: str = ""):
    """Checks children of two asts by iterating their fields

    Parameters
    ----------
    left : ast.AST
        the student code
    right : ast.AST
        the solution code
    line_info :  Optional[Dict[str, int]], optional
        holds line information about a particular node, by default None
    last_parent : str, optional
        the nearest parent that can be converted to source text, by default ""
    left_source : str
        the source text for user code
    right_source : asttokens.ASTTokens
        the source text for the solution code
    """
    lf, rf = ast.iter_fields(left), ast.iter_fields(right)
    # iterate through the children of both ASTs
    for left_field, right_field in zip_longest(lf, rf, fillvalue=""):
        left_name, left_values = left_field
        right_name, right_values = right_field
        # attempt to get a new parent source text for feedback
        # check that the name of the AST nodes match
        compare_node(left_name, right_name, line_info, last_parent)
        # recurse on values
        compare_ast(left_values, right_values, line_info, last_parent, left_source, right_source,)

def compare_ast(left: ast.AST, 
                right: ast.AST, 
                line_info: Optional[Dict[str, int]] = None,
                last_parent: str = "",
                left_source: str = "", 
                right_source: str = "") -> None:
    """Compare two abstract syntax trees. Raise AssertionError as soon as they differ.

    Parameters
    ----------
    left : ast.AST
        the student code
    right : ast.AST
        the solution code
    line_info :  Optional[Dict[str, int]], optional
        holds line information about a particular node, by default None
    last_parent : str, optional
        the nearest parent that can be converted to source text, by default ""
    left_source : str
        the source text for user code
    right_source : asttokens.ASTTokens
        the source text for the solution code
    """
    # to hold line information like line number, and original source
    line_info = {} if line_info is None else line_info
    # check types first
    compare_node_type(left, right, line_info, last_parent)

    # the check AST, list of Expr, or a core data type
    if isinstance(left, ast.AST):
        # store line number for feedback
        line_info["left"] = getattr(
            left, "lineno", line_info.get("left", 1)
        )
        line_info["right"] = getattr(
            right, "lineno", line_info.get("right", 1)
        )
        # attempt to get a new parent source text for feedback
        last_parent = new_parent_source(left, last_parent)
        # for ast.Call we will raise error when there is either a problem 
        # with the function or the arguments do not match after standardization
        if isinstance(left, ast.Call):
            # check that the standardized left and right Calls are the same
            check_functions(left, right, line_info, last_parent, left_source, right_source)
        else:
            check_children(left, right, line_info, last_parent, left_source, right_source)
    elif isinstance(left, list):
        for left_child, right_child in zip_longest(left, right, fillvalue=""):
            # recurse on [Expr, ...]
            # attempt to get a new parent source text for feedback
            last_parent = new_parent_source(left_child, last_parent)
            compare_ast(left_child, right_child, line_info, last_parent, left_source, right_source)
    else:
        compare_node(left, right, line_info, last_parent)

# TODO document
def check_functions(left_call: ast.AST, 
                   right_call: ast.AST, 
                   line_info: Optional[Dict[str, int]] = None,
                   last_parent: str = "",
                   left_source: str = "", 
                   right_source: str = ""):
    """Standardizes and compares two ast.Calls. Raise AssertionError as soon as they differ.

    Parameters
    ----------
    left_call : ast.AST
        the user function call
    right_call : ast.AST
        the solution function call
    line_info :  Optional[Dict[str, int]], optional
        holds line information about a particular node, by default None
    last_parent : str, optional
        the nearest parent that can be converted to source text, by default ""
    left_source : str
        the source text for user code
    right_source : asttokens.ASTTokens
        the source text for the solution code
    """
    # standardize the left and right tree
    ls = standardize_arguments(left_call, left_source)
    rs = standardize_arguments(right_call, right_source)
    # if we don't have any arguments simply compare the two nodes
    if len(ls.keywords) == 0:
        check_children(left_call, right_call, line_info, last_parent, left_source, right_source,)
    for l, r in zip_longest(ls.keywords, rs.keywords, fillvalue=""):
        wrong_value(ls, rs, line_info, last_parent, formatted(l.value) == formatted(r.value))
    
def compare_node_type(
        left: Any, 
        right: Any,
        line_info: Dict[str, int],
        last_parent: str
    ) -> None:
    """Compare two ASTs' types and raise an exception with the line number if different.

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
    """
    # str stands for "empty", so if user code is missing something, present 
    # a message about missing expectation  
    if isinstance(left, str) and not isinstance(right, str):
        missing(left, right, line_info)
    # otherwise, present a message about unexpected user's AST
    elif not isinstance(left, str):
        # if we do expect a certain AST, point out that expectation
        if not isinstance(right, str):
            wrong_value(left, right, line_info, last_parent, type(left) == type(right))
        # otherwise, just state what was not expected
        else:
            not_expected(left, right, line_info)

def compare_node(left: Any, right: Any, line_info: Dict[str, int], last_parent: str):
    """Compare two objects of the same type and raise an exception with feedback if nodes differ.

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
    """
    wrong_value(left, right, line_info, last_parent, left == right)

def grade_code(student_code: str, solution_code: str):
    """Checks user and solution code and prints a message if they differ

    Parameters
    ----------
    student_code : str
        the user source code
    solution_code : str
        the solution source code

    Returns
    -------
    None
        If there are no issues
    str
        If user code differs from solution
    """
    try:
        # source node back
        student = ast.parse(student_code)
        solution = ast.parse(solution_code)
        # set parent node of child nodes for better feedback
        last_parent = formatted(next(n for n in ast.walk(student)))
        compare_ast(student, solution, last_parent = last_parent, left_source=student_code, right_source=solution_code)
    except AssertionError as e:
        return str(e) # back to either the python_grader or python_grade_learnr
    except Exception as e:
        return "There was a problem checking user or solution code: {}".format(e)

if __name__ == "__main__":
    # TODO move to testing class
    # these are the non-verbose cases
    test_cases = [
        # different core types
        ("\"1\"", "1", "I expected 1, but what you wrote was interpreted as \"1\" at line 1."),
        ("1", "\"1\"", "I expected \"1\", but what you wrote was interpreted as 1 at line 1."),
        ("[1]", "\"1\"", "I expected \"1\", but what you wrote was interpreted as [1] at line 1."),
        ("True", "\"1\"", "I expected \"1\", but what you wrote was interpreted as True at line 1."),
        ("False", "\"1\"", "I expected \"1\", but what you wrote was interpreted as False at line 1."),
        # str vs str
        ("\"not hello\"", "\"hello\"", "I expected \"hello\", but what you wrote was interpreted as \"not hello\" at line 1."),
        # list vs list
        ("[2]", "[]", "I did not expect 2 at line 1."),
        ("[1,2]", "[1]", "I did not expect 2 at line 1."),
        ("[1]", "[1,2]", "I expected 2 at line 1."),
        # expr vs something else
        ("1 + 1", "1", "I expected 1, but what you wrote was interpreted as 1 + 1 at line 1."),
        ("1 + (2 + 2)", "1 + (2 + 3)", "I expected 3, but what you wrote was interpreted as 2 in 2 + 2 at line 1."),
        ("-1", "1", "I expected 1, but what you wrote was interpreted as -1 at line 1."),
        # functions
        # TODO this is an odd one, maybe we could just revert to original source text for these?
        ("2 + sum([1,2])", "2 + sum([1,1])", "I expected sum(iterable=[1, 1], start=0), but what you wrote was interpreted as sum(iterable=[1, 2], start=0) at line 1."),
        ("sqrt(log(2))", "sqrt(log(1))", "I expected 1, but what you wrote was interpreted as 2 in log(2) at line 1."),
        ("def foo(a, b=1): pass; foo(2)", "def foo(a, b=1): pass; foo(1)", "I expected foo(a=1, b=1), but what you wrote was interpreted as foo(a=2, b=1) at line 1."),
        ("def foo(a, b=1): pass; foo(a=2)", "def foo(a, b=1): pass; foo(1)", "I expected foo(a=1, b=1), but what you wrote was interpreted as foo(a=2, b=1) at line 1."),
        ("def foo(a, b=1): pass; foo(a=[2])", "def foo(a, b=1): pass; foo(2, 2)", "I expected foo(a=2, b=2), but what you wrote was interpreted as foo(a=[2], b=1) at line 1."),
        ("def foo(a, b=1): pass; foo(a=\"2\", b=2)", "def foo(a, b=1): pass; foo(2, 2)", "I expected foo(a=2, b=2), but what you wrote was interpreted as foo(a=\"2\", b=2) at line 1."),
        ("def head(n=5): pass; head(12)", "def head(n=5): pass; head(n=10)", "I expected head(n=10), but what you wrote was interpreted as head(n=12) at line 1."),
    ]
    for t in test_cases:
        print("~~~")
        print("user code:\n{}\n".format(t[0]))
        print("solution code:\n{}\n".format(t[1]))
        message = grade_code(t[0], t[1])
        print(message)
        if message != t[2]:
            raise ValueError(
                "Failed test case!\nUser:{}\nSolution:{}\nExpected:{}\nGot:{}".format(
                    t[0],
                    t[1],
                    t[2],
                    message
                )
            )
    print("All tests passed! :)")
