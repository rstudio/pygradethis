
#' Wrapper for `pygradecode.find_arguments.args()`
#'
#' In Python, the args() function takes positional (*args) 
#' and keyword (**kwargs). Similarly, `py_args()` can also take
#' arbitrary number of positional and named arguments.
#'
#' NOTE: the value of arguments still have to be passed as `character()`
#' @export
py_args <- function(...) {
  find_arguments_mod$args(...)
}

#' Wrapper for `pygradecode.find_arguments.find_arguments()`
#' @export
py_find_arguments <- function(code = .user_code, match = py_args(), env = parent.frame()) {
  find_arguments_mod$find_arguments(code, match)
}