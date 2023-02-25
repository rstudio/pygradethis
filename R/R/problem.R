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
return_if_problem <- function(problem, env = parent.frame()) {
  if (is_pygradethis_problem(problem)) {
    rlang::return_from(env, problem)
  }
  NULL
}

catch_internal_problem <- function(expr, ...) {
  tryCatch(expr, ..., error = function(err) {
    message("An error occurred in the grading code: ", err$message)
    pygradethis::problem("pygradethis_internal", error = err$message)
  })
}

return_if_internal_problem <- function(expr, ..., env = parent.frame()) {
  prob <- catch_internal_problem(expr, ...)
  return_if_problem(prob, env = env)
}

#' @export
problem_grade.pygradethis_internal_problem <- function(
  problem, max_diffs = 3, env = parent.frame(), ...
) {
  # move error up to top-level of grade
  error <- problem$error
  problem$error <- NULL

  gradethis::graded(
    message = paste(
      "Uh-oh! We can't provide feedback at this time. Don't worry, it's not",
      "your fault! There's an issue behind-the-scenes with this exercise."
    ),
    correct = logical(0),
    type = "warning",
    location = "replace",
    problem = problem,
    error = error
  )
}

#' @export
problem_message.wrong_index_problem <- function(problem, ...) {
  # if there are values for both actual and expected give some
  # more feedback on what the difference is
  extra <- NULL
  if (!is.null(problem$actual) && !is.null(problem$expected)) {
    extra <- tblcheck::problem_message(
      tblcheck::vec_check(problem$actual, problem$expected, env = env)
    )
  }

  glue::glue("{problem$message} {extra}", .null = "")
}

#' @export
problem_message.wrong_columns_problem <- function(problem, ...) {
  # check if we have a difference of types
  extra <- NULL

  # if there's a class problem return feedback for that
  class_problem <- tblcheck::tbl_check_class(
    problem$actual,
    problem$expected,
    env = env
  )
  if (tblcheck::is_tblcheck_problem(class_problem)) {
    extra <- tblcheck::problem_message(class_problem)
  } else {
    # otherwise, just provide the incorrect values feedback
    values_problem <- tblcheck::vec_check(
      problem$actual,
      problem$expected,
      env = env
    )
    extra <- tblcheck::problem_message(values_problem)
  }

  glue::glue("{problem$message} {extra}", .null = "")
}

#' @export
problem_message.wrong_values_problem <- function(problem, ...) {
  # if there are values for both actual and expected give some
  # more feedback on what the difference is
  extra <- NULL
  if (!is.null(problem$actual) && !is.null(problem$expected)) {
    extra <- tblcheck::problem_message(
      tblcheck::vec_check(problem$actual, problem$expected, env = env)
    )
  }
  glue::glue("{problem$message} {extra}", .null = "")
}

#' @export
problem_message.wrong_series_problem <- function(problem, ...) {
  extra <- NULL
  if (!is.null(problem$actual) && !is.null(problem$expected)) {
    extra <- tblcheck::problem_message(
      tblcheck::vec_check(problem$actual, problem$expected, env = env)
    )
  }
  glue::glue("{problem$message} {extra}", .null = "")
}

#' Generic problem with the result
#' @export
problem_message.pygradethis_problem <- function(problem, ...) {
  problem$message
}

#' Generic problem with the code
#' @export
problem_message.pygradecode_problem <- function(problem, ...) {
  problem$message
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

#' @export
problem_grade.pygradecode_problem <- function(
    problem, max_diffs = 3, env = parent.frame(), ...
) {
  problem_grade.pygradethis_problem(problem, max_diffs, env)
}
