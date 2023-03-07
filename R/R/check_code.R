
#' @export
py_find_functions <- function(code = .user_code, match = character(1), env = parent.frame()) {
  find_functions$find_functions(code, match)
}

#' @export
py_find_lambdas <- function(code = .user_code, env = parent.frame()) {
  find_functions$find_lambdas(code)
}
