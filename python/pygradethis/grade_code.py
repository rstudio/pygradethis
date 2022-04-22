"""
This module is used to check if a user's code is equal to solution code and
note when the two differ.
"""

# parsing
import ast

# formatting
from .formatters import formatted
# checking functions
from .check_functions import standardize_arguments
# feedback
from .message_generators import (
    missing, not_expected, wrong_value, repeated_argument
)

# misc
from itertools import zip_longest
from typing import Dict, Any

def new_parent_source(tree: Any, last_parent: str) -> str:
    """Given an ast, the current tree, and the last parent source,
    return a new last parent source for facilitating feedback on problematic
    node.

    Parameters
    ----------
    tree : Any
        the ast.AST or a Python type we want to extract the source text for
    last_parent : str
        the nearest parent that can be converted to source text

    Returns
    -------
    str
        the new last_parent or the same
    """
    # only set the last_parent if:
    # 1) it is a somewhat complex AST which is defined as having more than 1 field, 
    # wich means that for e.g. "1" is not a good candidate since we're trying to support
    # calling out higher level expressions
    # 2) we can get a source text
    if (len(tree._fields) > 1 and 
        (issubclass(tree.__class__, ast.Expr) or issubclass(tree.__class__, ast.Call))):
        # attempt to get a new parent source text for feedback
        try:
            last_parent = formatted(tree)
        except:
            pass
    return last_parent
    
def check_children(left: Any, 
                   right: Any, 
                   line_info: Dict[str, int],
                   left_source: str = "", 
                   right_source: str = "",
                   last_parent: str = ""):
    """Checks children of two asts by iterating their fields

    Parameters
    ----------
    left : ast.AST
        the student code
    right : ast.AST
        the solution code
    line_info :  Dict[str, int]]
        holds line information about a particular node
    left_source : str, optional
        the source text for user code, by default ""
    right_source : str, optional
        the source text for the solution code, by default ""
    last_parent : str, optional
        the nearest parent that can be converted to source text, by default ""
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
        compare_ast(left_values, right_values, line_info, left_source, right_source, last_parent)

def compare_ast(left: Any, 
                right: Any, 
                line_info: Dict[str, int],
                left_source: str = "", 
                right_source: str = "",
                last_parent: str = "") -> None:
    """Compare two abstract syntax trees. Raise AssertionError as soon as they differ.

    Parameters
    ----------
    left : Any
        the student code
    right : Any
        the solution code
    line_info :  Dict[str, int]]
        holds line information about a particular node
    left_source : str
        the source text for user code, by default ""
    right_source : str
        the source text for the solution code, by default ""
    last_parent : str
        the nearest parent that can be converted to source text, by default ""
    """
    # to hold line information like line number, and original source
    line_info = {} if line_info is None else line_info
    # check types first
    compare_node_type(left, right, line_info)

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
            check_functions(left, right, line_info, left_source, right_source, last_parent)
        else:
            check_children(left, right, line_info, left_source, right_source, last_parent)
        
    elif isinstance(left, list):
        for left_child, right_child in zip_longest(left, right, fillvalue=""):
            # recurse on [Expr, ...]
            # attempt to get a new parent source text for feedback
            compare_ast(left_child, right_child, line_info, left_source, right_source, last_parent)
    else:
        compare_node(left, right, line_info, last_parent)

def check_functions(left_call: ast.Call, 
                   right_call: ast.Call, 
                   line_info: Dict[str, int],
                   left_source: str = "", 
                   right_source: str = "",
                   last_parent: str = ""):
    """Standardizes and compares two ast.Calls. Raise AssertionError as soon as they differ.

    Parameters
    ----------
    left_call : ast.Call
        the user function call
    right_call : ast.Call
        the solution function call
    line_info :  Dict[str, int]]
        holds line information about a particular node
    last_parent : str
        the nearest parent that can be converted to source text, by default ""
    left_source : str
        the source text for user code, by default ""
    right_source : str
        the source text for the solution code, by default ""
    """
    # TODO standardize_arguments args naming is confusing, perhaps refactor it.
    # standardize the left and right tree
    ls = standardize_arguments(left_call=left_call, right_call=right_call, left_source=left_source, right_source=right_source)
    rs = standardize_arguments(left_call=right_call, right_call=right_call, left_source=right_source, right_source=right_source)
    # if we don't have any arguments simply compare the two nodes
    if len(ls.keywords) == 0:
        check_children(left_call, right_call, line_info, left_source, right_source, last_parent)
    # else, check all of the arguments which are all in keywords after running
    # `standardize_arguments` to simplify checking
    if ls != None and rs != None:
        for l, r in zip_longest(ls.keywords, rs.keywords, fillvalue=""):
            # check if the student and solution keyword matches in their value
            wrong_value(l.value, r.value, line_info, formatted(l.value) == formatted(r.value), last_parent)
            # last parent node would be the value of the parameter if it's an expression/call
            last_parent = new_parent_source(l.value, last_parent)
    else:
        raise AssertionError("Foo-y! Something went wrong with function call checking.")
    
def compare_node_type(
        left: Any, 
        right: Any,
        line_info: Dict[str, int],
        last_parent: str = ""
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
    """
    # handle missing code
    if (isinstance(left, str) and left == '') and not isinstance(right, str):
        missing(left, right, line_info)
    elif left != '' and right == '':
        # handle case for an unexpected value
        not_expected(left, right, line_info)
    else:
        # or, wrong types
        wrong_value(left, right, line_info, type(left) == type(right), last_parent)

def compare_node(left: Any, right: Any, line_info: Dict[str, int], last_parent: str = ""):
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
    wrong_value(left, right, line_info, left == right, last_parent)

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
        if student_code == '':
            raise Exception("I didn't receive the student code.")
        elif solution_code == '':
            raise Exception("I didn't receive the solution code.")
        student = ast.parse(student_code)
        solution = ast.parse(solution_code)
        last_parent = [a for a in ast.walk(ast.parse(student))][1]
        compare_ast(
            student, 
            solution, 
            {}, 
            left_source = student_code, 
            right_source = solution_code, 
            last_parent = new_parent_source(last_parent, "")
        )
    except SyntaxError as e:
        message = str(e)
        # TODO figure out why we're getting unknown for diagnosis of argument
        if "repeated" in message:
            return repeated_argument(e)
    except AssertionError as e:
        return str(e) # back to either the python_grader or python_grade_learnr
    except Exception as e:
        return "There was a problem checking user or solution code: {}".format(e)
