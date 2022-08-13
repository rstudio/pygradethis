#' The main `pygradethis` module that can be used to access other
#' submodules and functions within the Python library.
#'
#' @return the `pygradethis` Python module
#' @export
pygradethis <- NULL

#' The `exercise.checker` pygradethis_exercise_checker to use in learnr
#'
#' @return the `pygradethis_exercise_checker` Python function
#' @export
pygradethis_exercise_checker <- NULL

#' Get the last value of Python source code
#'
#' @return the value
#' @export
get_last_value <- NULL

.onLoad <- function(libname, pkgname) {
  # import `pygradethis` and the exercise checking function
  pygradethis <<- reticulate::import("pygradethis", convert=FALSE, delay_load = TRUE)
  pygradethis_exercise_checker <<- pygradethis$pygradethis_exercise_checker$pygradethis_exercise_checker
  get_last_value <<- pygradethis$utils$get_last_value
  reticulate::py_run_string('import builtins', convert = FALSE)
}
