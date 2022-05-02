# pygradethis

[![PyPI version](https://badge.fury.io/py/pygradethis.svg)](https://badge.fury.io/py/pygradethis)
[![PyPI - License](https://img.shields.io/pypi/l/pygradethis)](LICENSE)
[![Downloads](https://pepy.tech/badge/pygradethis)](https://pepy.tech/project/pygradethis)

A Python package to facilitate checking code output or static code checking
using AST analysis. It can either be used with R using the [`learnr`](https://rstudio.github.io/learnr/) package, as 
a mirror of [`gradethis`](https://rstudio-education.github.io/gradethis/index.html) package, or as a standalone package for general Python 
use in educational settings.

**Note**: This package is in early development and will undergo rapid changes.

## Install

```
pip install pygradethis
```

## Dependencies

- Python 3.9+

## Dev Dependencies

- pytest

## Features

- Simple output checking based on pass / fail conditions with feedback
- Simple static code checking (AST), with feedback on how student's code differs from solution

## Output checks

`pygradethis` mimics the cadence to `gradethis::grade_result`. For e.g., we can
check that the student supplies the `mpg` dataset like so:

```python
python_grade_result(
  python_pass_if(mpg, "You also got the mpg dataframe!"),
  python_fail_if(None, "")
)
```

Internally, these `python_pass_if(output, message)` or `python_fail_if(output, message)` will be checked sequentially in
the order of arguments and return on first condition we match. The `None` here can be used
if you simply want to execute a condition if none of the other conditions matched.

If we match a `python_pass_if` or `python_fail_if`, we will present a feedback message wrapped in a convenient `dict`:

```python
dict(
    message = str,
    correct = True|False,
    type = "auto|success|info|warning|error|custom",
    location = "append|prepend|replace"
)
```

The `message` is the feedback, the `correct` is whether or not the student's solution is correct, `type` is the type of feedback. When 
used with `learnr` the `location` field here is useful for where the message is situated in the tutorial. However, for those using 
this package as a standalone the `location` is not an important field and it can be ignored. More on the flags [here](https://rstudio.github.io/learnr/exercises.html#Exercise_Checking).

Internally, a random praise/encouragement message will be appended before any custom message supplied. 

```python
python_pass_if(x = mpg, message = "You also got the mpg dataframe!")
```
Feedback:
> Bravo! You also got the mpg dataframe!

```python
python_fail_if(x = None, message = "")
```
Feedback:
> Try it again. You get better each time.

## Code checks

For static code checking, we follow a similar cadence for `gradethis::grade_code`. 

When there is a solution code being supplied, `grade_code(user_code, solution_code)` can be used to check the AST of
the user and solution code, making sure to standardize function calls and producing a helpful message for the student
to diagnose their issue.

Example:

```python
grade_code(
  student_code="2 + sqrt(log(2))", 
  solution_code="2 + sqrt(log(1))"
)

```
Feedback:
> I expected `log(1)`, but what you wrote was interpreted as `log(2)` in `sqrt(log(2))` at line 1.

Note how the feedback narrows in on the expression in which the problem occurs (`sqrt(log(2))`)
so that the student can focus on the most relevant outer expression of the problem. In this case, the 
`log(2)` is the problem and the `2` on the left operand of 
the addition is not as relevant.

Similarly, here the feedback points out that the 2 within the `log` function is incorrect, similar to the 
`gradethis` [example](https://rstudio-education.github.io/gradethis/reference/grade_code.html).

### Call Standardization
`pygradethis` also knows how to take user's function call code and map positional arguments 
to proper parameter names and set defaults if not supplied. This is so that you don't penalize
a student's code just because they did not explicitly spell out positional argument names, or
write the default arguments out.

For e.g. suppose a student is calling the following silly function `foo`:

```python
def foo(a, b=1): 
  pass
```

Grading the code with

```python
grade_code(
  student_code="foo(1)", 
  solution_code="foo(1)"
)
```

In the example above, the `grade_code` doesn't give us a feedback message since they are equivalent expressions.

However, if the student supplies `foo(2)`

```python
grade_code(
  student_code="foo(2)", 
  solution_code="foo(1)"
)
```

we get back this feedback:
> I expected `1`, but what you wrote was interpreted as `2` in `foo(2)` at line 1.

**Note:** Although underneath the hood we do standardize the arguments of both the student and the solution code
before checking, we don't surface this standardized form to the feedback message. This is certainly possible to
achieve but in certain cases can hinder learning by revealing too much information. For example, the builtin functions
like `sum` is normally called without specifying its actual formal parameters (e.g. `sum(1)` versus `sum(iterable=[1], start=0)`. In the future, a `verbose` mode could be made available such that the formal parameters are pointed out.

For call standardizing to work, the function definitions corresponding to function 
calls must be defined  and 'live' in the environment, whether that is the `globals()`/`locals()`,
`builtins`, or custom module imports `pandas`. This works if the student/solution source code also 
includes the definition (like `foo` above) in their own source code or it's included by instructor. 

Currently, common modules like `math` is imported for grading within `check_functions.py`, but more modules 
will be included to serve data science grading as well, such as `pandas` or `numpy` in the future. 
We plan to make the code more extensible for the instructor to add them as dependencies.
