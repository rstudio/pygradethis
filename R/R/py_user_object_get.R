
#' Retrieves an envir from checking envir such as
#' `.py_envir_result` or `.py_envir_solution`, or one of gradethis
#' objects like `.solution`
py_resolve_envir <- function(py_envir, check_env) {
  py_envir_label <- rlang::as_name(rlang::enexpr(py_envir))
  get0(py_envir_label, check_env, ifnotfound = NULL)
}

py_object_exists <- function(x, py_envir) {
  !is.null(reticulate::py_get_item(py_envir, x, silent = TRUE))
}

# User objects ----

#' Function for checking if a Python object was created by student code
#'
#' @param x An object name, given as a quoted `character` string.
#' @param check_env The `environment` from which to retrieve `.py_envir_result`
#'
#' @return logical
#' @export
py_user_object_exists <- function(x, check_env = parent.frame()) {
  .py_envir_result <- py_resolve_envir(.py_envir_result, check_env)
  py_object_exists(x, .py_envir_result)
}

#' Function for fetching an object created by student code
#'
#' @param x An object name, given as a quoted `character` string.
#' @param check_env The `environment` from which to retrieve `.py_envir_result`
#'
#' @return a Python object
#' @export
py_user_object_get <- function(x, py_envir, check_env = parent.frame()) {
  .py_envir_result <- py_resolve_envir(.py_envir_result, check_env)
  reticulate::py_get_item(.py_envir_result, x, silent = TRUE)
}

#' Function for fetching a `[character]` of variables from the student code.
#'
#' The list returned contain variables introduced beyond the ones in the
#' `.py_envir_prep` environment which is produced by the setup code.
#'
#' @param x An object name, given as a quoted `character` string.
#' @param check_env The `environment` from which to retrieve `.py_envir_result`
#'
#' @return a `[character]` vector
#' @export
py_user_object_list <- function(check_env = parent.frame()) {
  .py_envir_prep <- py_resolve_envir(.py_envir_prep, check_env)
  .py_envir_result <- py_resolve_envir(.py_envir_result, check_env)

  # get the difference of variables introduced by student code
  new_objs <- pygradethis::get_envir_diff(.py_envir_prep, .py_envir_result)
  res <- reticulate::py_to_r(new_objs)

  # order of variable names are not guaranteed so we sort it for convenience
  if (length(res)) {
    return(sort(res))
  }
  res
}

# Solution objects ----

#' Function for checking if an object was created by solution code
#'
#' @param x An object name, given as a quoted `character` string.
#' @param check_env The `environment` from which to retrieve `.py_envir_solution`
#'
#' @return logical
#' @export
py_solution_object_exists <- function(x, check_env = parent.frame()) {
  py_resolve_envir(.solution, check_env)
  .py_envir_solution <- py_resolve_envir(.py_envir_solution, check_env)
  py_object_exists(x, .py_envir_solution)
}

#' Function for fetching an object created by solution code
#'
#' @param x An object name, given as a quoted `character` string.
#' @param check_env The `environment` from which to retrieve `.py_envir_solution`
#'
#' @return a Python object
#' @export
py_solution_object_get <- function(x, check_env = parent.frame()) {
  py_resolve_envir(.solution, check_env)
  .py_envir_solution <- py_resolve_envir(.py_envir_solution, check_env)
  reticulate::py_get_item(.py_envir_solution, x, silent = TRUE)
}

#' Function for fetching a `[character]` of variables from the solution code.
#'
#' The list returned contain variables introduced beyond the ones in the
#' `.py_envir_prep` environment which is produced by the setup code.
#'
#' @param x An object name, given as a quoted `character` string.
#' @param check_env The `environment` from which to retrieve `.py_envir_solution`
#'
#' @return a `[character]` vector
#' @export
py_solution_object_list <- function(check_env = parent.frame()) {
  .py_envir_prep <- py_resolve_envir(.py_envir_prep, check_env)
  # the solution envir is delayed until we force/retrieve the .solution
  py_resolve_envir(.solution, check_env)

  .py_envir_solution <- py_resolve_envir(.py_envir_solution, check_env)

  # get the difference of variables introduced by solution code
  new_objs <- pygradethis::get_envir_diff(.py_envir_prep, .py_envir_solution)
  res <- reticulate::py_to_r(new_objs)

  # order of variable names are not guaranteed so we sort it for convenience
  if (length(res)) {
    return(sort(res))
  }
  res
}
