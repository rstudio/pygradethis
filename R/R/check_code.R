
#' @export
py_find_lambdas <- function(code = .user_code, env = parent.frame()) {
  code <- get0(".user_code", envir = env, ifnotfound = code)

  results <- find_functions$find_lambdas(code)

  if (length(results$elements)) {
    return(invisible(results))
  }

  tblcheck::problem_grade(
    problem(
      type = "pygradecode_problem",
      message = "I could not find any `lambda` in the code."
    )
  )
}