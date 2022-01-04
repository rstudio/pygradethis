"""
This module contains functions to check function calls, standardize arguments,
and return standardized call.
"""
import ast
import inspect
import builtins
from typing import Union
# add any libraries you might need for grading
# TODO we need a better way to include lib dependencies for running student code
from math import *

from .message_generators import (
    missing_argument, unexpected_argument, surplus_argument
)
from .formatters import formatted

def standardize_arguments(
    left_call: ast.Call, 
    right_call: ast.Call,
    left_source: str = "",
    right_source: str = "") -> Union[ast.Call, None]:
    """This will standardize the function calls for a function Call and return
    the modified Call.
    
    Returns None if there are no issues with the function call.
    
    Otherwise, an error message is returned if the user code can't be parsed,
    if there is a problem not finding variables in environment, or if arguments
    cannot be standardized.

    Parameters
    ----------
    left_call : ast.Call
        the user's function call to standardize arguments
    right_call : ast.Call
        the solution function call to standardize arguments
    left_source : str, optional
        the entire source code in which left_call belongs, by default ""
    right_source : str, optional
        the entire source code in which right_call belongs the source code, by default ""

    Returns
    -------
    ast.Call
        standardized function call

    Raises
    ------
    AssertionError
        when there is an issue with the standardization process
    """
    final_call = None
    try:
        # 1) introduce function call in environment
        # first pass: is it legal Python code?
        # for e.g., positional args should always be before keywords args
        # exec will catch these issues
        # NOTE: we are attempting to import `r` object for learnr use.
        if "r" in globals():
            exec(left_source, {}, r)
        else:
            exec(left_source)
        # 2) construct an environment containing both global and locals, 
        # overwriting the globals with locals, and builtins.
        envir = dict(globals(), **locals(), **builtins.__dict__)
        # 3) grab the live function from the environment
        # if we're calling a function on an object, the function info has
        # to be extracted from an ast.Attribute
        if isinstance(left_call.func, ast.Attribute):
            func_name = getattr(left_call.func, "attr")
            # the object's name 
            obj = left_call.func.value.id
            # the live function from the environment associated with object
            # e.g. the `df` in df.head() is a pd.DataFrame so must get the
            # `head` associated with that class.
            live_func = getattr(envir[obj], func_name)
        else:
            # if we're calling a function not associated with an object
            # just grab function from environment using its name
            func_name = left_call.func.id
            live_func = envir[func_name]

        # 4) collect the arguments passed
        # construct keyword args mapping
        kwargs = {a.arg: a.value for a in left_call.keywords}

        # 5) get the formal arguments for function
        sig = None
        try:
            # Note: this will raise ValueError if inspect cannot retrieve signature
            # which can happen for some builtins like `print`, where underlying C
            # code does not provide any metadata about its signature.
            sig = inspect.signature(live_func)
        except ValueError: 
            # if we can't get a signature just return call for normal Call
            # checking flow
            final_call = left_call
        if sig is None:
            raise ValueError()

        # 6) unpack args and kwargs and attempt to standardize argument calls
        # returns: https://docs.python.org/3.6/library/inspect.html#inspect.BoundArguments
        partial_args = sig.bind(*left_call.args, **kwargs)
        partial_args.apply_defaults()

        # 7) return a modified AST representing the standardized call
        # we do this by updating Call.keywords and reset the args
        new_keywords = []
        for k, v in partial_args.arguments.items():
            new_keywords.append(ast.keyword(arg=k, value=v))
        left_call.args = []
        left_call.keywords = new_keywords
        final_call = left_call
    except TypeError as e:
        # when call itself is invalid (e.g. wrong argument name)
        error = str(e)
        if "missing" in error:
            missing_argument(
                left_call,
                formatted(standardize_arguments(
                    left_call=right_call, right_call = right_call, 
                    left_source=right_source, right_source=right_source
                    )
                ),
                error
            )
        if "unexpected" in error:
            unexpected_argument(
                left_call,
                formatted(standardize_arguments(
                    left_call=right_call, right_call = right_call, 
                    left_source=right_source, right_source=right_source
                    )
                ),
                error
            )
        if "too many" in error:
            surplus_argument(
                left_call,
                formatted(standardize_arguments(
                    left_call=right_call, right_call = right_call, 
                    left_source=right_source, right_source=right_source
                    )
                ),
                error
            )
    except NameError as e:
        # when the function name doesn't exist in environment
        raise AssertionError(str(e).capitalize())
    except Exception as e:
        # when other Exceptions occur, silently ignore for now
        pass
    return final_call

if __name__ != '__main__':
  try:
    # attempt to import if used with R's `learnr` package
    from __main__ import r
  except:
    pass
