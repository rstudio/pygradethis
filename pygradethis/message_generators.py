"""
This module holds functions for common mistakes and generating messages for
feedback to the student.
"""

# TODO: use these from `python_grader`, `python_grade_learnr`, and `grade_code`

def wrong_value(this, that):

    # def foo(a, b=1): pass
    
    # foo(1)
    # foo(2)

    # "h(1), I expected 2 where you wrote 1."
    # "I expected {that} where you wrote {this}."
    pass


def duplicate_name(this_call, this_name):

    # def foo(a, b=1): pass

    # foo(a=1, a=2)
    # SyntaxError: keyword argument repeated

    # "You passed multiple arguments named {this_name} to {this_call}, which will cause "
    # "an error. Check your spelling, or remove one of the arguments."
    pass

def wrong_call(this, that):
    # def foo(a, b=1): pass

    # bar(1)
    # foo(1)

    # "I expected you to call {that} where you called {this}."
    pass

def bad_argument_name(this, this_name):
    # def foo(a, b=1): pass
    # foo(x=1)

    # TypeError: foo() got an unexpected keyword argument 'x'

    # {this} got an unexpected keyword argument {this_name}
    pass


def missing_argument(this, that_name):
    # def foo(a, b=1): pass
    # foo() missing 1 required positional argument: 'a'

    # "Your call to {this} should include {that_name} ",
    # "You may have misspelled an argument name, ",
    # "or left out an important argument."
    pass


def surplus_argument(this, this_arg):

    # def foo(a, b=1): pass
    # foo(x=1) => TypeError: foo() got an unexpected keyword argument 'x'

    # "I did not expect your call to {this} to ",
    # "include {this_arg}. You ",
    # "may have included an unnecessary argument, or you ",
    # "may have left out or misspelled an important ",
    # "argument name."
    pass
