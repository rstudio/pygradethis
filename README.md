# pygradethis

A Python package to facilitate checking code output or static code checking
using AST analysis. It can either be used with R using the [`learnr`](https://rstudio.github.io/learnr/) package, as 
a mirror of [`gradethis`](https://rstudio-education.github.io/gradethis/index.html) package, or as a standalone package for general Python 
use in educational settings.

**Note**: This package is in early development and will undergo rapid changes.

## Dependencies

- Python 3.6
- [asttokens](https://github.com/gristlabs/asttokens) *

*We rely on asttokens for getting the text back from a source node (if possible) for 
static AST checking (more on that below). Python 3.8 has an improved ast module which
can do away with this dependency in the future.

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

If we match a `python_pass_if`, we will present a feedback message wrapped in a convenient `Grader`
class:

```python
Graded(
    message = "a feedback message for success|error|warning events", 
    correct = True|False, 
    type = "success|error|warning", 
    location = "append"
  )
```

Internally, a random praise/encouragement message will be appended before any custom message supplied. 

`python_pass_if(mpg, "You also got the mpg dataframe!")`:
> Bravo! You also got the mpg dataframe!

`python_fail_if(None, "")`:
> Try it again. You get better each time.

When used with `learnr` the `location` field here is useful for where the message is situated in the tutorial.
However, for those using this package as a standalone the `location` is not an important field and it can be ignored.

## Code checks

For static code checking, we follow a similar cadence for `gradethis::grade_code`. 

When there is a solution code being supplied, `check_code(user_code, solution_code)` can be used to check the AST of
the user and solution code, making sure to standardize function calls and producing a helpful message for the student
to diagnose their issue.

Example 1:

```python
check_code("2 + sum([1,2])", "2 + sum([1,1])")
```
Feedback:
> I expected 1, but you wrote 2 in `[1,2]` at line 1.

Note how the expression in which the problem occurs (`[1,2]`) is pointed out so that the student is aware that the `2`
within the list is incorrect not the left operand of the binary operation.

Example 2:

```python
check_code("sqrt(log(2))", "sqrt(log(1))")
```
Feedback:
> I expected 1, but you wrote 2 in `log` at line 1.

Similarly, here the feedback points out that the 2 within the `log` function is incorrect, similar to the 
`gradethis` [example](https://rstudio-education.github.io/gradethis/reference/grade_code.html).

Currently, standardizing implementation is in progress but the idea is to take user's function call code
and map positional arguments to proper parameter names and set defaults if not supplied.

For e.g. `head(10)` => `head(n=10)`.



