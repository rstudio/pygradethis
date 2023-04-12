
#' Wrapper for `pygradecode.find_arguments.args()`
#'
#' In Python, the args() function takes positional (*args)
#' and keyword (**kwargs). Similarly, `py_args()` can also take
#' arbitrary number of positional and named arguments.
#'
#' NOTE: the value of arguments still have to be passed as `character()`
#' @export
#' @param ... Any number of (un)named arguments
py_args <- function(...) {
  find_arguments_mod$args(...)
}

#' Wrapper for `pygradecode.find_arguments.find_arguments()`
#'
#' @param code The user code character
#' @param match A `py_args()` to specify arguments and keyword arguments
#' @param env The grading environment
#'
#' @export
py_find_arguments <- function(code = .user_code, match = py_args(), env = parent.frame()) {
  find_arguments_mod$find_arguments(code, match)
}

#' A Python class used to represent a literal string
#'
#' @param source A `character` representing code
#' @export
py_literal <- function(source) {
  pygradecode$xml_utils$literal(source)
}
