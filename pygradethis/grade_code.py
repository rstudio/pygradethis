"""
This module is used to check if a user's code is equal to solution code and
note when the two differ.
"""

# parsing
import parser
import ast
import asttokens
# formatting
from .formatters import formatted
# misc
from itertools import zip_longest
from typing import Optional, Dict, Any

# TODO allow this to be enabled via CLI + function param
# verbose mode includes the expression for the problematic node in feedback
VERBOSE = False

def new_parent_source(atok: asttokens.ASTTokens, tree: Any, last_parent: str):
    """Given the token-marked ast, the current tree, and the last parent source,
    return a new last parent source for facilitating feedback on problematic
    node.

    Parameters
    ----------
    atok : asttokens.ASTTokens
        the token-marked AST
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
    parent_source = atok.get_text(tree)
    # only set the `last_parent` if:
    # - it is a compound ast, and
    # - we can get a source text
    if isinstance(tree, ast.AST) and len(tree._fields) > 1 and parent_source != "":
        last_parent = parent_source
    return last_parent

def compare_ast(atok: asttokens.ASTTokens,
                left: ast.AST, 
                right: ast.AST, 
                line_info: Optional[Dict[str, int]] = None,
                last_parent: str = "") -> None:
    """Compare two abstract syntax trees. Raise AssertionError as soon as they differ.

    Parameters
    ----------
    atok : asttokens.ASTTokens
        the token-marked AST for the student code
    left : ast.AST
        the student code
    right : ast.AST
        the solution code
    line_info :  Optional[Dict[str, int]], optional
        holds line information about a particular node, by default None
    last_parent : str, optional
        the nearest parent that can be converted to source text, by default ""
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
        lf, rf = ast.iter_fields(left), ast.iter_fields(right)
        # iterate through the children of both ASTs
        for left_field, right_field in zip_longest(lf, rf, fillvalue=""):
            left_name, left_values = left_field
            right_name, right_values = right_field
            # attempt to get a new parent source text for feedback
            last_parent = new_parent_source(atok, left_values, last_parent)
            # check that the name of the AST nodes match
            compare_node(left_name, right_name, line_info, last_parent)
            # recurse on values
            compare_ast(atok, left_values, right_values, line_info, last_parent)
    elif isinstance(left, list):
        for left_child, right_child in zip_longest(left, right, fillvalue=""):
            # recurse on [Expr, ...]
            # attempt to get a new parent source text for feedback
            last_parent = new_parent_source(atok, left_child, last_parent)
            compare_ast(atok, left_child, right_child, line_info, last_parent)
    else:
        compare_node(left, right, line_info, last_parent)

def compare_node_type(
        left: Any, 
        right: Any, 
        line_info: Dict[str, int],
        last_parent: str
    ) -> None:
    """Compare two ASTs' types and raise an exception with the line number if different.

    Parameters
    ----------
    lleft : Any
        an ast.Node, a custom type, or a python data type
    right : Any
        an ast.Node, a custom type, or a python data type
    line_info : Dict[str, int]
        holds line information about a particular node
    last_parent : str
        the nearest parent that can be converted to source text
    """
    # TODO find a more maintaible way to handle the string setup for feedback here
    # str stands for "empty", so if user code is missing something, present 
    # a message about missing expectation  
    if isinstance(left, str) and not isinstance(right, str):
        msg = "I expected {} at line {}."
        msg_args = (
            formatted(right), 
            line_info.get("left")
        )
        if VERBOSE:
            msg = "I expected {} in `{}` at line {}."
            msg_args = (
                formatted(right), 
                last_parent,
                line_info.get("left")
            )
    # otherwise, present a message about unexpected user's AST
    elif not isinstance(left, str):
        # if we do expect a certain AST, point out that expectation
        if not isinstance(right, str):
            msg = "I did not expect {} at line {}. I expected {}."
            msg_args = (
                formatted(left), 
                line_info.get("left"),
                formatted(right)
            )
            # if we want to include expression in feedback, grab the source text
            if VERBOSE:
                msg = "I did not expect {} in `{}` at line {}. I expected {}."
                msg_args = (
                    formatted(left),
                    last_parent,
                    line_info.get("left"),
                    formatted(right)
                )
        # otherwise, just state what was not expected
        else:
            msg = "I did not expect {} at line {}."
            msg_args = (
                formatted(left), 
                line_info.get("left")
            )
            if VERBOSE:
                msg = "I did not expect {} in `{}` at line {}."
                msg_args = (
                    formatted(left), 
                    last_parent,
                    line_info.get("left")
                )
    
    assert type(left) == type(right), msg.format(*msg_args)

def compare_node(
        left: Any, 
        right: Any, 
        line_info: Dict[str, int],
        last_parent: str
    ):
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
    msg = "I expected {}, but you wrote {} at line {}."
    msg_args = (
        formatted(right), 
        formatted(left),
        line_info.get("left"),
    )
    if VERBOSE:
        msg = "I expected {}, but you wrote {} in `{}` at line {}."
        msg_args = (
            formatted(right),
            formatted(left),
            last_parent,
            line_info.get("left"),
        )
    assert left == right, msg.format(*msg_args)


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
        # TODO: make parser more pluggable for 3.8 ast parser or other potential parsers like antlr
        # with the contract being it needs a similar `get_text` for getting
        # source node back
        student = asttokens.ASTTokens(student_code, parse=True)
        solution = asttokens.ASTTokens(solution_code, parse=True)
        # set parent node of child nodes for better feedback
        atok = student
        last_parent = atok.get_text(next(n for n in ast.walk(atok.tree)))
        compare_ast(atok, student.tree, solution.tree, last_parent = last_parent)
    except AssertionError as e:
        return str(e)
    except Exception as e:
        return "There was a problem checking user or solution code: {}".format(e)

if __name__ == "__main__":
    # TODO move to testing class
    VERBOSE = False
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
        ("[1]", "[1,2]", "I expected 2 at line 1."),
        # func vs func
        ("len([1,2,3])", "sum([1,2,3])", "I expected \"sum\", but you wrote \"len\" at line 1."),
        ("sum([1,2])", "sum([1,2,3])", "I expected 3 at line 1."),
        ("df.head()", "df.head(10)", "I expected 10 at line 1."),
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
        print("~~~")
        print("user code:\n{}\n".format(t[0]))
        print("solution code:\n{}\n".format(t[1]))
        message = grade_code(t[0], t[1])
        # print(message)
        if message != t[2]:
            raise ValueError(
                "Failed test case!\nUser:{}\nSolution:{}\nExpected:{}\nGot:{}".format(
                    t[0],
                    t[1],
                    t[2],
                    message
                )
            )
    print("All tests passed for non-verbose messages! :)")
    # also test verbose cases
    VERBOSE = True
    # TODO add more cases for verbose message style
    # TODO decided whether we should stick with verbose mode by default or not
    test_cases_verbose = [
        ("1", "\"1\"", "I did not expect 1 in `1` at line 1. I expected \"1\"."),
        ("[1]", "\"1\"", "I did not expect list in `[1]` at line 1. I expected \"1\"."),
        ("[1,2]\n2", "[1]", "I did not expect 2 in `[1,2]` at line 1."),
        ("2 + sum([1,2])", "2 + sum([1,1])", "I expected 1, but you wrote 2 in `[1,2]` at line 1."),
        ("sqrt(log(2))", "sqrt(log(1))", "I expected 1, but you wrote 2 in `log` at line 1."),
    ]
    for t in test_cases_verbose:
        print("~~~")
        print("student code:\n{}\n".format(t[0]))
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
    print("All tests passed for verbose messages! :)")
