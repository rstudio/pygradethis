
#' @export
py_find_functions <- function(code = .user_code, match = character(1), env = parent.frame()) {
  gcf <- find_functions$find_functions(code, match)

  if (length(gcf$results)) {
    return(gcf)
  }

  tblcheck::problem_grade(
    problem(
      type = "pygradecode_problem",
      message = "I could not find any `function` call in the code."
    )
  )
}

#' @export
py_find_lambdas <- function(code = .user_code, env = parent.frame()) {
  gcf <- find_functions$find_lambdas(code)

  if (length(gcf$results)) {
    return(gcf)
  }

  tblcheck::problem_grade(
    problem(
      type = "pygradecode_problem",
      message = "I could not find any `lambda` in the code."
    )
  )
}
