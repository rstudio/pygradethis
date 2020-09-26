"""
This module contains functions to check function calls, standardize arguments,
and return standardized call.
"""
import ast
import inspect
import builtins

from .formatters import formatted
from math import sqrt, log

from itertools import zip_longest

def standardize_arguments(call: ast.Call, source_code: str) -> ast.Call:
    """This will standardize the function calls for a function Call and return
    the modified Call.
    
    Returns None if there are no issues with the function call.
    
    Otherwise, an error message is returned if the user code can't be parsed, 
    if there is a problem not finding variables in environment, or if arguments 
    cannot be standardized.

    Parameters
    ----------
    call : ast.Call
        the call to standardize arguments
    source_code : str
        the source code in which the call belongs to

    Returns
    -------
    ast.Call
        the standardized call

    Raises
    ------
    TypeError
        when call itself is invalid (e.g. wrong argument name)
    NameError
        when for e.g. the function name doesn't exist in environment
    Exception
        when other Exceptions occur, silently ignore for now
    """
    try:
        # 1) introduce function call in environment
        # first pass: is it legal Python code?
        # for e.g., positional args should always be before keywords args
        # exec will catch these issues
        exec(source_code)
        # 2) construct a environment containing encompassing both global and locals, 
        # overwriting the globals with locals, and builtins.
        envir = dict(globals(), **locals(), **builtins.__dict__)
        # 3) grab the live function from the environment
        # if we're calling a function on an object, the function info has
        # to be extracted from an ast.Attribute
        if isinstance(call.func, ast.Attribute):
            func_name = getattr(call.func, "attr") 
            # the object's name 
            obj = call.func.value.id
            # the live function from the environment associated with object
            # e.g. the `df` in df.head() is a pd.DataFrame so must get the
            # `head` associated with that class.
            live_func = getattr(envir[obj], func_name)
        else:
            # if we're calling a function not associated with an object
            # just grab function from environment using its name
            func_name = call.func.id
            live_func = envir[func_name]

        # 4) collect the arguments passed
        # construct keyword args mapping
        kwargs = {a.arg:a.value for a in call.keywords}
        
        # 5) get the formal arguments for function
        try:
            # Note: this will raise ValueError if inspect cannot retrieve signature
            # which can happen for some builtins like `print`, where underlying C
            # code does not provide any metadata about its signature.
            sig = inspect.signature(live_func)
        except ValueError: 
            # if we can't get a signature just return call for normal Call
            # checking flow
            return call

        # 6) unpack args and kwargs and attempt to standardize argument calls
        # returns: https://docs.python.org/3.6/library/inspect.html#inspect.BoundArguments
        partial_args = sig.bind(*call.args, **kwargs)
        partial_args.apply_defaults()

        # 7) return a modified AST representing the standardized call
        # we do this by updating Call.keywords and reset the args
        new_keywords = []
        for k, v in partial_args.arguments.items():
            new_keywords.append(ast.keyword(arg=k, value=v))
        call.args = []
        call.keywords = new_keywords
        return call
    except TypeError as e:
        raise AssertionError(str(e).capitalize())
    except NameError as e:
        raise AssertionError(str(e).capitalize())
    except Exception as e:
        pass
