# pygradethis 0.4.0

* Added helper functions to check existence of or retrieve user objects (`py_user_object_list()`, `py_user_object_exists()`, `py_user_object_get()`)
  or solution objects (`py_solution_object_list()`, `py_solution_object_exists()`, `py_solution_object_get()`)
* A new `.py_envir_prep` object that is the Python environment before any student code is run
* A `get_envir_diff()` wrapper around Python function of same name that looks at the difference of variables
  between two dictionaries (Python environments)

# pygradethis 0.3.0

* Added code checking support via `pygradecode` Python package through find functions and friends
* Added find functions `py_find_functions()`, `py_find_lambdas()`, and `py_find_arguments()`
* Added helper functions `py_literal()`, `py_args()`
* Added `py_fail_if_not_found()` and `py_fail_if_found()` to facilitate grading find functions

# pygradethis 0.2.2

* Added object type validation for `check_*()` functions
* Speed up tests with a `with_py_clear_env()` helper function to clear out Python environment 
  after every `test_that()` call instead of the slower `callr::r_safe()`
* Replace deprecated functions for `dplyr` and `gradecode`

# pygradethis 0.2.1

* Added identical() generic that wraps base::identical() and provides type-specific methods for R objects converted from Python
* Added waldo::compare_proxy() methods for R objects converted from Python to fix waldo::compare() behavior

# pygradethis 0.2.0

* Validate inputs for the `check_*()` functions
* Improve the grading feedback around unexpected types by leveraging `tblcheck` generics `friendly_class()` and `hinted_class_message()`

