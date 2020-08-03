"""
This module is used to check if a user's code is equal to solution code and
note when the two differ.
"""

# parsing
import parser
import ast
import asttokens
# formatting
from formatters import formatted
# misc
from itertools import zip_longest
from typing import Optional, Dict, Any

# TODO allow this to be enabled via CLI + function param
# verbose mode includes the expression for the problematic node in feedback
VERBOSE = False

def compare_ast(left: ast.AST, right: ast.AST, line_info: Optional[Dict[str, int]] = None) -> None:
    """
    Compare two abstract syntax trees. Raise an exception as soon as they differ.
    """
    # to hold line information like line number, and original source
    line_info = {} if line_info is None else line_info
    left_tree = getattr(left, "tree", left)
    right_tree = getattr(right, "tree", right)

    # check types first
    compare_node_type(left_tree, right_tree, line_info)

    # check AST, list of Expr, or a core data type
    if isinstance(left_tree, ast.AST):
        # store line number for feedback
        line_info["left"] = getattr(
            left_tree, "lineno", line_info.get("left", 1)
        )
        # store away the problematic node source text for verbose feedback
        if isinstance(left, asttokens.ASTTokens) and len(left.tree._fields) >= 1:
            line_info["left_source"] = left.get_text(left_tree)

        line_info["right"] = getattr(
            right_tree, "lineno", line_info.get("right", 1)
        )
        # iterate through the fields of both ASTs
        left_fields = ast.iter_fields(left_tree)
        right_fields = ast.iter_fields(right_tree)
        for left_field, right_field in zip_longest(left_fields, right_fields, fillvalue=""):
            left_name, left_values = left_field
            right_name, right_values = right_field
            # check that the name of the AST nodes match
            compare_node(left_name, right_name, line_info)
            # recurse on values
            compare_ast(left_values, right_values, line_info)
    elif isinstance(left_tree, list):
        for left_child, right_child in zip_longest(left_tree, right_tree, fillvalue=""):
            compare_ast(left_child, right_child, line_info)
    else:
        compare_node(left_tree, right_tree, line_info)

def compare_node_type(left: Any, right: Any, line_info: Dict[str, int]) -> None:
    """
    Compare two objects. Return "" if equal, and raise an exception with 
    the line number otherwise.
    """
    # TODO find a more maintaible way to handle the string setup for feedback here
    # str stands for "empty", so if user code is missing something, present 
    # a message about missing expectation  
    if isinstance(left, str) and not isinstance(right, str):
        msg = "I expected {} on line {}."
        msg_args = (
            formatted(right), 
            line_info.get("left")
        )
    # otherwise, present a message about not expected
    elif not isinstance(left, str) and not isinstance(right, str):
        msg = "I did not expect {} at line {}. I expected {}."
        msg_args = (
            formatted(left), 
            line_info.get("left"),
            formatted(right)
        )
        if "left_source" in line_info and VERBOSE:
            msg = "I did not expect {} in `{}` at line {}."
            msg_args = (
                formatted(left), 
                line_info.get("left_source"),
                line_info.get("left")
            )
    elif not isinstance(left, str) and isinstance(right, str):
        msg = "I did not expect {} at line {}."
        msg_args = (
            formatted(left), 
            line_info.get("left")
        )
        if "left_source" in line_info and VERBOSE:
            msg = "I did not expect {} in `{}` at line {}."
            msg_args = (
                formatted(left), 
                line_info.get("left_source"),
                line_info.get("left")
            )
    assert type(left) == type(right), msg.format(*msg_args)

def compare_node(left: Any, right: Any, line_info: Dict[str, int]) -> str:
    """
    Compare two objects of the same type and raise an exception with feedback if nodes differ.
    """
    msg = "I expected {}, but you wrote {} at line {}."
    msg_args = (
        formatted(right), 
        formatted(left),
        line_info.get("left"),
    )
    if "left_source" in line_info and VERBOSE:
        msg = "I expected {}, but you wrote {} in `{}` at line {}."
        msg_args = (
            formatted(right),
            formatted(left),
            line_info.get("left_source", ""),
            line_info.get("left"),
        )
    assert left == right, msg.format(*msg_args)

def check_code(user_code, solution_code):
    """Checks user and solution code and prints a message if they differ"""
    try:
        # TODO use token-marked ast so we can get node's source text for feedback
        user = asttokens.ASTTokens(user_code, parse=True)
        solution = asttokens.ASTTokens(solution_code, parse=True)
        compare_ast(user, solution)
    except AssertionError as e:
        return str(e)
    except Exception as e:
        return "There was a problem checking user or solution code: {}".format(e)

if __name__ == "__main__":
    # TODO move to testing class
    # these are the non-verbose cases
    test_cases = [
        # different core types
        ("\"1\"", "1", "I did not expect \"1\" at line 1. I expected 1."),
        ("1", "\"1\"", "I did not expect 1 at line 1. I expected \"1\"."),
        ("[1]", "\"1\"", "I did not expect list at line 1. I expected \"1\"."),
        ("True", "\"1\"", "I did not expect True at line 1. I expected \"1\"."),
        ("False", "\"1\"", "I did not expect False at line 1. I expected \"1\"."),
        # str vs str
        ("\"not hello\"", "\"hello\"", "I expected \"hello\", but you wrote \"not hello\" at line 1."),
        # list vs list
        ("[2]", "[]", "I did not expect 2 at line 1."),
        ("[1,2]", "[1]", "I did not expect 2 at line 1."),
        ("[1]", "[1,2]", "I expected 2 on line 1."),
        # func vs func
        ("len([1,2,3])", "sum([1,2,3])", "I expected \"sum\", but you wrote \"len\" at line 1."),
        ("sum([1,2])", "sum([1,2,3])", "I expected 3 on line 1."),
        ("df.head()", "df.head(10)", "I expected 10 on line 1."),
        ("df.shape", "df.head(10)", "I did not expect \"shape\" on df at line 1. I expected the function \"head\"."),
        ("df.head(n=10)", "df.head()", "I did not expect the keyword argument \"n\" at line 1."),
        # TODO use check_arguments() for argument standardization; make these 2 pass
        # ("df.head(n=10)", "df.head(10)", "I did not expect the keyword argument \"n\" at line 1."),
        # ("def foo(a, n=2): pass; foo(2)", "def foo(a, n=2): pass; foo(a=2)", ""),
        # expr vs something else
        ("1 + 1", "1", "I did not expect an arithmetic expression at line 1. I expected 1."),
        ("-1", "1", "I did not expect an unary operator at line 1. I expected 1."),
    ]
    for t in test_cases:
        # print("\nuser code: {}".format(t[0]))
        # print("\nsolution code: {}\n\n".format(t[1]))
        message = check_code(t[0], t[1])
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




