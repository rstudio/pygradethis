# pygradethis ----

#' @noRd
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
pygradethis <- inform_python_pygradethis_not_found

#' The `exercise.checker` pygradethis_exercise_checker to use in learnr
#'
#' @return the `pygradethis_exercise_checker` Python function
#' @export
#' @keywords internal
pygradethis_exercise_checker <- inform_python_pygradethis_not_found

#' Get the last value of Python source code
#'
#' @return the value
#' @export
#' @keywords internal
get_last_value <- inform_python_pygradethis_not_found

#' Find the difference of variables created in prepped versus student environment
#' 
#' This is used to find new variables introduced in `.py_envir_result`
#' excluding the `.py_envir_prep` setup environment
#'
#' @return the list of key strings
#' @export
#' @keywords internal
get_envir_diff <- inform_python_pygradethis_not_found

# pygradecode ----

#' The `pygradecode` module that contains code checking functions.
#'
#' @return the `pygradecode` Python module
#' @export
pygradecode <- inform_python_pygradethis_not_found

#' The `pygradecode.find_functions` module containing functions to
#' check for function calls.
#'
#' @return the Python module pygradecode.find_functions
#' @export
find_functions_mod <- inform_python_pygradethis_not_found

#' The Python module `pygradecode.find_arguments` containing functions
#' to check for arguments within function calls.
#'
#' @return the Python module pygradecode.find_arguments
#' @export
find_arguments_mod <- inform_python_pygradethis_not_found

# Import Python functionality ----

.onLoad <- function(libname, pkgname) {
  gradethis::gradethis_setup(
    # `fail.encourage` lets `gradethis` generate a random
    # encouraging message when students give wrong answers.
    fail.encourage = TRUE,
    # `pass.praise` lets `gradethis` generate a random
    # positive message when students give correct answers.
    pass.praise = TRUE,
  )

  # set default messages
  # NOTE: this is a bit hacky solution for now for default messages
  # there's probably a better way to not flood options()
  # for e.g. using some kinda method dispatch via S3 or maybe `problem_message()`?
  options(
    'find_functions.fail_if_not_found' = "I could not find any `function` call in the code.",
    'find_functions.fail_if_found' = "I did not expect to find a `function` call.",
    'find_lambdas.fail_if_not_found' = "I could not find any `lambda` in the code.",
    'find_lambdas.fail_if_found' = "I did not expect to find a `lambda` in the code."
  )

  # import `pygradethis`, `pygradecode`, relevant modules and functions
  if (reticulate::py_available(initialize = TRUE)) {
    tryCatch({
      # Top level modules ----
      pygradethis <<- reticulate::import("pygradethis", convert=FALSE, delay_load = TRUE)
      pygradecode <<- reticulate::import("pygradecode", convert=FALSE, delay_load = TRUE)

      # pygradethis ----
      pygradethis_exercise_checker <<- pygradethis$pygradethis_exercise_checker$pygradethis_exercise_checker
      get_last_value <<- pygradethis$utils$get_last_value
      get_envir_diff <<- pygradethis$utils$get_envir_diff

      # pygradecode ----
      find_functions_mod <<- pygradecode$find_functions
      find_arguments_mod <<- pygradecode$find_arguments

      # we use builtins a lot so we import that module automatically
      reticulate::py_run_string('import builtins', convert = FALSE)
    }, error = function(err) {
      packageStartupMessage(
        "An error occurred while trying to connect {pygradethis} in R to the Python companion package:\n",
        conditionMessage(err)
      )
    })
  } else {
    inform_python_pygradethis_not_found(throw = message)
  }
}
