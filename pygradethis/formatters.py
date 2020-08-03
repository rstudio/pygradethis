
"""
Module contains a generic AST node formatter and allows for custom formatters
for whichever data type you need.

To define a node formatter simply define another `_` function, register its 
type for the generic `formatted` function, and define the string to return:

```
@formatted.register(<your type>)
def _(node):
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
from functools import singledispatch

@singledispatch
def formatted(node):
    """Generic function to return a formatted representation of an AST node"""
    return "{}".format(type(node).__name__.lower())

@formatted.register(str)
def _(el):
    """Formatting function for an str"""
    return "\"{}\"".format(el)

@formatted.register(int)
def _(el):
    """Formatting function for an int"""
    return "{}".format(el)

@formatted.register(ast.Expr)
def _(node):
    """Formatting function for an ast.Expr"""
    return "an expression"

@formatted.register(ast.Call)
def _(node):
    """Formatting function for an ast.Call"""
    if isinstance(node.func, ast.Attribute):
        func_name = getattr(node.func, "attr") 
    else:
        func_name = node.func.id
    return "the function \"{}\"".format(func_name)

@formatted.register(ast.keyword)
def _(node):
    """Formatting function for an ast.keyword"""
    return "the keyword argument \"{}\"".format(getattr(node, "arg"))

@formatted.register(ast.BinOp)
def _(node):
    """Formatting function for an ast.BinOp"""
    # for now, just punt to a generic string
    return "an arithmetic expression"

@formatted.register(ast.UnaryOp)
def _(node):
    """Formatting function for an ast.UnaryOp"""
    # for now, just punt to a generic string
    return "an unary operator"

@formatted.register(ast.Attribute)
def _(node):
    """Formatting function for an ast.Attribute"""
    return "\"{}\" on {}".format(getattr(node, "attr"), formatted(getattr(node, "value")))

@formatted.register(ast.Name)
def _(node):
    """Formatting function for an ast.Name"""
    return getattr(node, "id")

@formatted.register(ast.Num)
def _(node):
    """Formatting function for an ast.Num"""
    return getattr(node, "n")

@formatted.register(ast.Str)
def _(node):
    """Formatting function for an ast.Num"""
    return "\"{}\"".format(getattr(node, "s"))

@formatted.register(ast.NameConstant)
def _(node):
    """Formatting function for True/False"""
    return "{}".format(getattr(node, "value"))

def format_node(node_type, string_format):
    """Registers a format function for a give node type
    
    The node_type must be a valid data type in Python.
    The string_format can be either a str or a function / lambda.
    """
    @formatted.register(node_type)
    def _(node):
        if callable(string_format):
            return string_format(node)
        else:
            return string_format

