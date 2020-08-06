"""
This module contains functions to check function calls, standardize arguments,
and return standardized call.
"""
import inspect
import ast
import builtins

def check_arguments(source_code: str):
    """This will standardize the function calls within the user's source code
    and check if it can be standardized. 
    
    Returns None if there are no issues with the function call.
    
    Otherwise, an error message is returned if the user code can't be parsed, 
    if there is a problem not finding variables in environment, or if arguments 
    cannot be standardized.
    """
    try:
        # 1) introduce function call in environment
        # first pass: is it legal Python code?
        # for e.g., positional args should always be before keywords args
        # exec will catch these issues
        # TODO re: check if we really have to exec the user code or not 
        exec(source_code)
        # 2) get the ast tree
        tree = ast.parse(source_code)
        # 3) grab ast.Call nodes
        call_nodes = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
        # 4) construct a environment containing encompassing both global and locals, 
        # overwriting the globals with locals, and builtins.
        envir = dict(globals(), **locals(), **builtins.__dict__)
        # for each ast.Call
        for c in call_nodes:
            # 5) grab the live function from the environment
            # if we're calling a function on an object, the function info has
            # to be extracted from an ast.Attribute
            if isinstance(c.func, ast.Attribute):
                func_name = getattr(c.func, "attr") 
                # the object's name 
                obj = c.func.value.id
                # the live function from the environment associated with object
                # e.g. the `df` in df.head() is a pd.DataFrame so must get the
                # `head` associated with that class.
                live_func = getattr(envir[obj], func_name)
            else:
                # if we're calling a function not associated with an object
                # just grab function from environment using its name
                func_name = c.func.id
                live_func = envir[func_name]

            # 6) collect the arguments passed
            # construct keyword args mapping
            kwargs = {a.arg:a.value for a in c.keywords}
            
            # 7) get the formal arguments for function
            # Note: this will raise ValueError if inspect cannot retrieve signature
            # which can happen for some builtins like `print`, where underlying C
            # code does not provide any metadata about its signature.
            sig = inspect.signature(live_func)

            # 8) unpack args and kwargs and attempt to standardize argument calls
            # returns: https://docs.python.org/3.6/library/inspect.html#inspect.BoundArguments
            partial_args = sig.bind(*c.args, **kwargs)
            partial_args.apply_defaults()
            # TODO return a modified AST representing the standardized call
    except TypeError as e: # when call itself is invalid (e.g. wrong argument name)
        return e
    except NameError as e: # when for e.g. the function name doesn't exist in environment
        return e
    except ValueError as e: # when signature can't be retrieved, silently ignore for now
        pass

if __name__ == "__main__":
    # TODO move to testing class
    test_cases = [
"""
# user defined function
def head(n=1):
    pass
head(2)
""",
"""
# module defined function
import pandas as pd
df = pd.DataFrame({'a':[1,2,3]})
df.head(2)
"""
    ]
    for t in test_cases:
        result = check_arguments(t)
        assert result == None, (
            "test case failed: {}".format(t)
        )
    print("All tests passed! :)")
