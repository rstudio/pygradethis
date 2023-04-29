
#' Wrapper for `pygradecode.find_functions.find_functions()`
#'
#' See `help('pygradecode.find_arguments.find_arguments')` in Python for more details
#' 
#' @param code A `character` representing the code text.
#' @param match A `character` vector of function names.
#' @param env The environment which you don't have to worry for practical uses.
#'
#' @return A Python list[Element]
#' @export
py_find_functions <- function(
  code = .user_code,
  match = character(1),
  env = parent.frame()
) {
  code <- get_placeholder(code, env)

  found <- pygradethis:::catch_internal_problem({
    find_functions_mod$find_functions(code, match)
  })

  if (is_pygradethis_problem(found)) {
    return(tblcheck::problem_grade(found))
  }

  found
}

#' Wrapper for `pygradecode.find_functions.uses_function()`
#'
#' See `help('pygradecode.find_arguments.uses_function')` in Python for more details
#' 
#' @param code A `character` representing the code text.
#' @param match A `character` vector of function names.
#' @param env The environment which you don't have to worry for practical uses.
#'
#' @return A Python list[Element]
#' @export
py_uses_function <- function(
  code = .user_code,
  match = character(1),
  env = parent.frame()
) {
  code <- get_placeholder(code, env)

  found <- pygradethis:::catch_internal_problem({
    find_functions_mod$uses_function(code, match)
  })

  if (is_pygradethis_problem(found)) {
    return(tblcheck::problem_grade(found))
  }

  reticulate::py_to_r(found)
}

#' Wrapper for `pygradecode.find_functions.find_lambdas()`
#' 
#' See `help('pygradecode.find_arguments.find_lambdas')` in Python for more details
#' 
#' @param code A `character` representing the code text.
#' @param env The environment which you don't have to worry for practical uses.
#'
#' @return A Python list[Element]
#' @export
py_find_lambdas <- function(code = .user_code, env = parent.frame()) {
  code <- get_placeholder(code, env)

  found <- pygradethis:::catch_internal_problem({
    find_functions_mod$find_lambdas(code)
  })

  if (is_pygradethis_problem(found)) {
    return(tblcheck::problem_grade(found))
  }

  found
}
