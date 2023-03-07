

#' Return a failing grade based on the result of a find function
#'
#' The `py_fail_if_not_found()` is a version of `gradecode::fail_if_not_found()`
#' with the difference being that it uses the `tblcheck::problem_grade()` method
#' to signal a `problem` that `pygradethis` will respond to with a `gradethis::fail()`
#'
#' @param gradecode_found a `pygradecode.GradeCodeFound` Python object.
#' @param message a character.
#' @param env the parent.frame() environment as default or another environment.
#'
#' @return either a `pygradecode.GradeCodeFound` object or a `gradethis::fail()`
#' @export
#' @examples
#' \dontrun{
#' .user_code = '2 + 2'
#' # you can signal a failing grade by following a `py_find_*`() with `py_fail_if_not_found()`
#' # this example has no custom message for the fail(), where it will pick the default
#' # value in options() for the type of request (e.g. `find_lambas.fail_if_found`)
#' py_find_lambdas() %>%
#'   py_fail_if_not_found()
#' }
py_fail_if_not_found <- function(
  gradecode_found, message = NULL, env = parent.frame()
) {
  # If a query was successful, pass through
  if (length(gradecode_found$last_result) > 0) {
    return(invisible(gradecode_found))
  }

  # get the request type
  request_type <- reticulate::py_to_r(gradecode_found$get_last_state()$type)
  # so that we can use the default or user-supplied message
  # as the feedback for the `gradethis::fail()`
  msg <-
    switch(
      request_type,
      'find_functions.fail_if_not_found' = getOption('find_functions.fail_if_not_found'),
      'find_lambdas.fail_if_not_found' = getOption('find_lambdas.fail_if_not_found'),
      NULL
    )

  tblcheck::problem_grade(
    problem(
      type = "pygradecode_problem",
      message = msg %||% message
    )
  )
}

#' Signal a failing grade if something is to be found in the code
#'
#' `py_fail_if_found()` is the opposite of `py_fail_if_not_found()` where
#' if the last result was successful, we signal a `gradethis::fail()`
#'
#' @param gradecode_found a `pygradecode.GradeCodeFound` Python object.
#' @param message a character.
#' @param env the parent.frame() environment as default or another environment.
#'
#' @return either a `pygradecode.GradeCodeFound` object or a `gradethis::fail()`
#' @export
#' @examples
#' \dontrun{
#' # an example that contains two lambdas, but we're only focused on the
#' # one inside of `round()` so we attempt to find_lambdas() after finding all
#' # function calls with `find_functions('round')`
#' .user_code = 'round((lambda x: x + 0.5)(2))'
#'
#' py_find_functions(match = 'round') %>%
#'   py_find_lambdas() %>%
#'   py_fail_if_found()
#' }
py_fail_if_found <- function(
  gradecode_found, message = NULL, env = parent.frame()
) {
  # If a query was unsuccessful, return nothing
  if (length(gradecode_found$last_result) == 0) {
    return(invisible(gradecode_found))
  }

  # get the request type
  request_type <- reticulate::py_to_r(gradecode_found$get_last_state()$type)
  # so that we can use the default or user-supplied message
  # as the feedback for the `gradethis::fail()`
  msg <-
    switch(
      request_type,
      'find_functions.fail_if_found' = getOption('find_functions.fail_if_found'),
      'find_lambdas.fail_if_found' = getOption('find_lambdas.fail_if_found'),
      NULL
    )
  
  tblcheck::problem_grade(
    problem(
      type = "pygradecode_problem",
      message = msg %||% message
    )
  )
}