import inspect
import ast
import asttokens
import builtins

user_code = (
"""
def head(n=1):
    pass
head(10)
"""
)

# TODO now make it work for pandas calls and attributes
def check_parameters(user_code):
    """This will standardize the function calls within the user's source code
    and check if it can be standardized. 

    Still in early development.
    """
    # first pass: is it legal Python code?
    # for e.g., positional args should always be before keywords args
    try:
        exec(user_code)
        # 1) get the token-marked ast
        atok = asttokens.ASTTokens(user_code, parse=True)
        # 2) grab call nodes
        call_nodes = [n for n in ast.walk(atok.tree) if isinstance(n, ast.Call)]
        # 3) for each Call, inspect the arguments passed vs formal arguments
        for c in call_nodes[:]:
            # print(c.__dict__)
            # TODO handle the attribute call case as well
            attr_node = [n for n in ast.walk(c.func) if isinstance(n, ast.Attribute)]

            # try to get the live function from either the globals or the builtins
            live_func = locals()[c.func.id] if c.func.id in locals() else builtins.__dict__[c.func.id]
            kwargs = {}
            # construct keyword args mapping (TODO: see if there's a simpler way)
            for a in c.keywords:
                kwargs[a.arg] = a.value
            
            # grab formal parameters
            # Note: this will raise ValueError if inspect cannot retrieve signature
            # which can happen for some builtins like `print`, where underlying C
            # code does not provide any metadata about its signature.
            sig = inspect.signature(live_func)

            # unpack args and kwargs and attempt to standardize parameter calls
            partial_args = sig.bind(*c.args, **kwargs)
            partial_args.apply_defaults()
            # https://docs.python.org/3.6/library/inspect.html#inspect.BoundArguments
            # print(partial_args.arguments)
            return "you're good!"
    except TypeError as e:
        return 'user error: {}'.format(e)
    except ValueError as e:
        pass

print(check_parameters(user_code))


