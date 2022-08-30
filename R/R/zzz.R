inform_python_pygradethis_not_found <- function(..., throw = stop) {
  throw(
    "Python or the Python pygradethis package were not found when {pygradethis} was loaded. ",
    "Please verify your pygradethis or Python installation and restart your R session."
  )
}

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
pygradethis_exercise_checker <- inform_python_pygradethis_not_found

#' Get the last value of Python source code
#'
#' @return the value
#' @export
get_last_value <- inform_python_pygradethis_not_found

.onLoad <- function(libname, pkgname) {
  # import `pygradethis` and the exercise checking function
  if (reticulate::py_available(initialize = TRUE)) {
    tryCatch({
      pygradethis <<- reticulate::import("pygradethis", convert=FALSE, delay_load = TRUE)
      pygradethis_exercise_checker <<- pygradethis$pygradethis_exercise_checker$pygradethis_exercise_checker
      get_last_value <<- pygradethis$utils$get_last_value
      reticulate::py_run_string('import builtins', convert = FALSE)
    }, error = function(err) {
      message(
        "An error occurred while trying to connect {pygradethis} in R to the Python companion package:\n",
        conditionMessage(err)
      )
    })
  } else {
    print(reticulate::py_available())
    inform_python_pygradethis_not_found(throw = message)
  }
}
