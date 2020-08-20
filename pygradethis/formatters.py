
"""
Module contains a generic AST node formatter and allows for custom formatters
for whichever data type you need.

To define a node formatter simply define another `_` function, register its 
type for the generic `formatted` function, and define the string to return:

```
@formatted.register(<your type>)
def _(node: ast.AST) -> str:
    <process your node>
    return "<your string>"
```

Alternatively, you can also call the `format_node` function to register your
function using one of two ways:

1. `format_node(int, <"a string">)`

2. `format_node(int, <a function or lambda that formats and returns string>)`

The basic data types and ast types have been supported but can be changed in
the respective register function definition, or overriden with `format_node`.
"""

import ast
import astunparse
from functools import singledispatch

@singledispatch
def formatted(node: ast.AST) -> str:
    """Generic function to return a formatted representation of an AST node"""
    try:
        # astunparse adds \n to left/right so we strip it
        return astunparse.unparse(node).strip()
    except SyntaxError:
        return "{}".format(type(node).__name__.lower())

def format_node(node_type, string_format):
    """Registers a format function for a give node type
    
    The node_type must be a valid data type in Python.
    The string_format can be either a str or a function / lambda.
    """
    @formatted.register(node_type)
    def _(node: ast.AST) -> str:
        if callable(string_format):
            return string_format(node)
        else:
            return string_format

# binary operators
format_node(ast.Add, "+")
format_node(ast.Sub, "-")
format_node(ast.Mult, "*")
format_node(ast.MatMult, "@")
format_node(ast.Div, "/")
format_node(ast.FloorDiv, "//")
format_node(ast.Mod, "%")
format_node(ast.Pow, "**")
format_node(ast.LShift, "<<")
format_node(ast.RShift, ">>")
format_node(ast.BitOr, "|")
format_node(ast.BitXor, "^")
format_node(ast.BitAnd, "&")
# unary operators
format_node(ast.UAdd, "+")
format_node(ast.USub, "-")
format_node(ast.Invert, "~")
# bool operators
format_node(ast.And, "and")
format_node(ast.Or, "or")
format_node(ast.Not, "not")
# compare operators
format_node(ast.Eq, "==")
format_node(ast.NotEq, "!=")
format_node(ast.Lt, "<")
format_node(ast.LtE, "<=")
format_node(ast.Gt, ">")
format_node(ast.GtE, ">=")
format_node(ast.Is, "is")
format_node(ast.IsNot, "is not")
format_node(ast.In, "in")
format_node(ast.NotIn, "not in")

def uunparse(node: ast.AST) -> str:
    """Return a unparsed representation of an AST with added parens removed.

    Returns
    -------
    str
        unparsed node
    """
    # astunparse adds \n to left/right so we strip it
    unparsed = astunparse.unparse(node).strip() 
    return unparsed[1:-1]

# core types ------------------------------------------

@formatted.register(ast.Lambda)
@formatted.register(ast.Compare)
@formatted.register(ast.BoolOp)
@formatted.register(ast.BinOp)
def _(node: ast.AST) -> str:
    """Formatting function for:
    
    ast.Lambda
    ast.Compare
    ast.BoolOp
    ast.BinOp

    Parameters
    ----------
    node : ast.AST
        the ast node

    Returns
    -------
    str
        unparsed node
    """
    return uunparse(node)
