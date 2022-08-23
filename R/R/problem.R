#' @importFrom tblcheck problem_message
#' @importFrom tblcheck problem_grade
NULL

#' Declare a problem
#'
#' This is a shim around `tblcheck::problem` for constructing a `pygradethis_problem`
#' to communicate the problem that was discovered during checking.
#'
#' @param type A character string, e.g. `columns`, `index`, or `values` that
#'   describes the problem that was discovered.
#' @param expected actual The expected and actual values. These should be
#'   included when the value is a summary, e.g. `nrow(expected)` or
#'   `length(actual)`. Be careful not to include large amounts of data.
#' @param ... Additional elements to be included in the `problem` object.
#'
#' @keywords internal
#' @export
problem <- function(
  type, expected = NULL, actual = NULL, correct = FALSE, ...
) {
  tblcheck::problem(
    type = type,
    expected = expected,
    actual = actual,
    ...,
    .class = c(paste0(type, "_problem"), "pygradethis_problem")
  )
}

is_pygradethis_problem <- function(x, type = NULL) {
  inherits(x, "pygradethis_problem") &&
  (is.null(type) || inherits(x, paste0(type, "_problem")))
}

#' Helper function to return early from `py_check_*` functions
#'
#' This is especially useful when returning from checking functions that
#' combine multiple checks
#'
#' @param problem A `pygradethis_problem` object.
#' @param env The environment from which to return.
#'
#' @keywords internal
#' @noRd
return_if_problem <- function(problem, env = parent.frame()) {
  if (is_pygradethis_problem(problem)) {
    rlang::return_from(env, problem)
  }
  NULL
}

#' @export
problem_message.pygradethis_problem <- function(problem, ...) {
  problem$message
}

#' @export
problem_message.wrong_index_problem <- function(problem, ...) {
  extra <- tblcheck::tblcheck_message(
    tblcheck::vec_check(problem$actual, problem$expected, env = env)
  )
  glue::glue("{problem$message} {extra}")
}

#' @export
problem_message.wrong_columns_problem <- function(problem, ...) {
  # check if we have a difference of types
  actual_type <- get_friendly_class(problem$actual)
  class(problem$actual) <- actual_type
  expected_type <- get_friendly_class(problem$expected)
  class(problem$expected) <- expected_type

  # grade the types
  tblcheck::tbl_grade_class(problem$actual, problem$expected)

  # otherwise, just compare the values
  extra <- tblcheck::tblcheck_message(
    tblcheck::vec_check(problem$actual, problem$expected, env = env)
  )
  glue::glue("{problem$message} {extra}")
}

#' @export
problem_message.wrong_values_problem <- function(problem, ...) {
  extra <- tblcheck::tblcheck_message(
    tblcheck::vec_check(problem$actual, problem$expected, env = env)
  )
  glue::glue("{problem$message} {extra}")
}

#' @export
problem_message.wrong_series_problem <- function(problem, ...) {
  problem$message
}

#' @export
problem_message.wrong_series_problem <- function(problem, ...) {
  extra <- tblcheck::tblcheck_message(
    tblcheck::vec_check(problem$actual, problem$expected, env = env)
  )
  glue::glue("{problem$message} {extra}")
}

#' @export
problem_grade.pygradethis_problem <- function(
    problem, max_diffs = 3, env = parent.frame(), ...
) {
  if (is.null(problem)) {
    return(invisible())
  }

  gradethis::fail(
    tblcheck::problem_message(problem, max_diffs = max_diffs),
    problem = problem,
    env = env,
    ...
  )
}
