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

