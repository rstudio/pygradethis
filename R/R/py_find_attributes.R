
#' Wrapper for `pygradecode.find_attributes.find_properties()`
#'
#' @param code A character of the user code
#' @param match A character() of the property name, "" by default
#' @param env The grading environment
#'
#' @export
py_find_properties <- function(code = .user_code, match = character(1), env = parent.frame()) {
  code <- get_placeholder(code, env)
  
  found <- pygradethis:::catch_internal_problem({
    find_attributes_mod$find_properties(code, match)
  })

  if (is_pygradethis_problem(found)) {
    return(tblcheck::problem_grade(found))
  }

  found
}
