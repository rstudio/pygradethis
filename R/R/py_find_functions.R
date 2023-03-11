#' Wrapper for `pygradecode.find_functions.find_functions()`
#'
#' @param code A `character` representing the code text.
#' @param match A `character` vector of function names.
#' @param env The environment which you don't have to worry for practical uses.
#'
#' @return A Python list[Element]
#' See `help('pygradecode.find_arguments.find_arguments')` in Python for more details
py_find_functions <- function(code = .user_code, match = character(1), env = parent.frame()) {
  find_functions_mod$find_functions(code, match)
}

#' Wrapper for `pygradecode.find_functions.find_lambdas()`
#' 
#' @param code A `character` representing the code text.
#' @param env The environment which you don't have to worry for practical uses.
#'
#' @return A Python list[Element]
#' See `help('pygradecode.find_arguments.find_lambdas')` in Python for more details
py_find_lambdas <- function(code = .user_code, env = parent.frame()) {
  find_functions_mod$find_lambdas(code)
}
