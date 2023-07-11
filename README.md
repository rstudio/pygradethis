# pygradethis (WORK IN PROGRESS)

[![PyPI version](https://badge.fury.io/py/pygradethis.svg)](https://badge.fury.io/py/pygradethis)
[![PyPI - License](https://img.shields.io/pypi/l/pygradethis)](LICENSE)
[![lifecycle](https://img.shields.io/badge/lifecycle-experimental-blue.svg)](https://www.tidyverse.org/lifecycle/#experimental)

A Python package to facilitate checking code output or static code checking
using AST analysis. It can either be used with R using the [`learnr`](https://rstudio.github.io/learnr/) package, as 
a mirror of [`gradethis`](https://rstudio-education.github.io/gradethis/index.html) package, or as a standalone package for general Python 
use in educational settings.

**NOTE: This package is in early development and does not work yet!** Things may change drastically without warning during this early phase.

## Install pygradethis

The `pygradethis` package is composed of both Python and R packages. An R wrapper packages is required so we can use `pygradethis` with `learnr`. To install the package you will need to install both.

Go to the respective `./python` and `./R` directory, and install it with:

```
make install
```

## Install Dev Dependencies

To install Python development packages:

```
make install-dev
```

## Features

- Output checking common objects like DataFrames, Series, and more.
- Code checking (AST) for checking particular aspects like function calls.

## How it works

Currently, `pygradethis` provides a custom `exercise.checker` function called [`py_gradethis_exercise_checker`](https://github.com/rstudio/pygradethis/blob/6a3ffb7b114c810398597655eba1027337920788/R/R/exercise_checker.R#L115) to be used in `learnr` tutorials. It wraps the [`gradethis::gradethis_exercise_checker()`](https://pkgs.rstudio.com/gradethis/reference/gradethis_exercise_checker.html), which enables authors to use the same interface as `gradethis::grade_this()` to grade Python exercises inside of a `-check` chunk. Example:

```r
gradethis::grade_this({
  # code checking
  py_find_functions(match = "pivot") %>%
    py_fail_if_not_found(message = "Did you remember to call the `.pivot` function?")

  # result checking
  py_grade_dataframe()

  pass()
})
```

## Result checking

### Pandas specific objects

For result checking, there are several helper functions to grade objects from `pandas`:

- `py_grade_dataframe()` - Check if the student's DataFrame object matches the solutions
- `py_grade_series()` - Check if the student's Series object matches the solutions
- `py_grade_index()` - Check if the student's Index object matches the solutions

### Other Python objects

For any other checks, you have access to a few solution environment objects available to make this possible. The `.result`, `.solution` objects are converted Python objects in R (if possible), and the `.py_result`, `.py_solution` objects are the pure Python objects. 

This allows authors to use R code to check the `.result` and `.solution` objects using functions like `gradethis::pass_if_equal()`. 

For grading general Python objects, you can directly
do checks with the pure Python objects `.py_result` / `.py_solution` using `reticulate`. For example, you can check if the student and solution objects are equal:

```r
gradethis::grade_this({
  # result checking
  if (!reticulate::py_to_r(.py_solution$equals(.py_result))) {
    fail()
  }

  pass()
})
```

### Checking assigned objects

For most exercises, you will be grading the last expression, but there might be situations where you don't want students to return an object and instead grade an object stored in a variable. In this situation you can make use of two helper functions:

- `py_user_object_get("<variable>")` - Retrieve student object by name
- `py_user_object_get("<variable>")` - Retrieve solution object by name

Then, you can proceed to grade them using `reticulate`.

## Code checking

The static code checking is still early development, but there are two main helper functions exposed by the R package that can help cover most of the cases:

- `py_find_functions()` - Check if the code contains functions or certain functions
- `py_find_arguments()` - Check if the code contains certain function arguments

Each one of these can return all function calls or all arguments in the code, but also provide a `match` argument to target specfic ones. For example, here's how you can check the student code contains a `.pivot()` call, and fail if not found:

```r
py_find_functions(match = "pivot") %>%
  py_fail_if_not_found()
```

You can also target a specific argument with `py_find_arguments` using a `match` argument and a helper function called `py_args()` that accepts a variable number of arguments (`...`), that are either just a `"value"` or a `param="value"`, where the value has to be a Python code string:

```r
py_find_arguments(match = py_args("4", x = "2", y = "'Hello, World!'")) %>%
  py_fail_if_not_found()
```
