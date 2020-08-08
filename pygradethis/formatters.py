
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

# core types

@formatted.register(str)
def _(el):
    """Formatting function for an str"""
    return "\"{}\"".format(el)

@formatted.register(int)
def _(el):
    """Formatting function for an int"""
    return el

@formatted.register(ast.List)
def _(node):
    """Formatting function for an ast.List"""
    return [formatted(n) for n in node.elts]

@formatted.register(ast.Tuple)
def _(node):
    """Formatting function for an ast.Tuple"""
    return tuple([formatted(n) for n in node.elts])

@formatted.register(ast.Set)
def _(node):
    """Formatting function for an ast.Set"""
    return {formatted(n) for n in node.elts}

@formatted.register(ast.Dict)
def _(node):
    """Formatting function for an ast.Dict"""
    adict = {}
    for k, v in zip(node.keys, node.values):
        if isinstance(k, ast.Str):
            adict[k.s] = formatted(v)
        else:
            adict[formatted(k)] = formatted(v)
    return adict

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
    # grab args and keywords
    args = ""
    for i, a in enumerate(node.args):
        args += str(formatted(a))
        if i + 1 < len(node.args):
            args += ", "
    for j, k in enumerate(node.keywords):
        args += "{}={}".format(k.arg, formatted(k.value))
        if j + 1 < len(node.keywords):
            args += ", "
    # return call like it would appear
    return "{}({})".format(func_name, args)

@formatted.register(ast.keyword)
def _(node):
    """Formatting function for an ast.keyword"""
    return getattr(node, "arg")

@formatted.register(ast.BinOp)
def _(node):
    """Formatting function for an ast.BinOp"""
    # for now, just punt to a generic string
    return "{} {} {}".format(formatted(node.left), formatted(node.op), formatted(node.right))

@formatted.register(ast.UnaryOp)
def _(node):
    """Formatting function for an ast.UnaryOp"""
    # for now, just punt to a generic string
    return "{}{}".format(formatted(node.op), formatted(node.operand))

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
    """Formatting function for an ast.Str"""
    return "\"{}\"".format(getattr(node, "s"))

@formatted.register(ast.NameConstant)
def _(node):
    """Formatting function for True/False"""
    return getattr(node, "value")
