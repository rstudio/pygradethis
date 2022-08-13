
return_if_problem <- function(problem, env = parent.frame()) {
  if (!is.null(problem)) {
    rlang::return_from(env, problem)
  }
}

#' Get the index of a pandas.DataFrame/pandas.Series
#'
#' @param data A DataFrame/Series.
#'
#' @return An Inex
#' @export
#' @examples
#' # ADD_EXAMPLES_HERE
get_index <- function(data) {
  data$index
}

#' Get the columns of a pandas.DataFrame/pandas.Series
#'
#' @param data A DataFrame/Series.
#'
#' @return An np.array of values
#' @export
#' @examples
#' # ADD_EXAMPLES_HERE
get_columns <- function(data) {
  data$columns
}

#' Get the values of a pandas.DataFrame/pandas.Series
#'
#' @param data A DataFrame/Series.
#'
#' @return An np.array of values
#' @export
#' @examples
#' # ADD_EXAMPLES_HERE
get_values <- function(data) {
  data$values
}

#' Checks that the Index of two DataFrame/Series are the same.
#'
#' Extracts the values out of the Index to do the check.
#'
#' @param object A DataFrame/Series to be compared to `expected`.
#' @param expected A DataFrame/Series containing the expected column.
#'
#' @return A TRUE if equal, FALSE otherwise
#' @export
#' @examples
#' # ADD_EXAMPLES_HERE
check_index <- function(object = .result, expected = .solution, env = parent.frame()) {
  if (inherits(object, ".result")) {
    object <- get(".result", env)
  }
  if (inherits(expected, ".solution")) {
    expected <- get(".solution", env)
  }
  left_vals <- translate(get_index(object))
  right_vals <- translate(get_index(expected))
  identical(left_vals, right_vals)
}

#' Checks that the columns of two DataFrame/Series are the same.
#'
#' This extracts columns from the two objects, converts them to R lists 
#' and checks that they are identical.
#'
#' @param object A DataFrame/Series to be compared to `expected`.
#' @param expected A DataFrame/Series containing the expected column.
#'
#' @return A TRUE if equal, FALSE otherwise
#' @export
#' @examples
#' # ADD_EXAMPLES_HERE
check_columns <- function(object = .result, expected = .solution, env = parent.frame()) {
  if (inherits(object, ".result")) {
    object <- get(".result", env)
  }
  if (inherits(expected, ".solution")) {
    expected <- get(".solution", env)
  }
  # extract and translate column values
  obj_vals <- translate(get_columns(object))
  exp_vals <- translate(get_columns(expected))
  identical(obj_vals, exp_vals)
}

#' Checks that the values of two DataFrame/Series are the same.
#'
#' This extracts values from the two objects, converts them to R lists
#' and checks that they are identical.
#'
#' @param object A DataFrame/Series to be compared to `expected`.
#' @param expected A DataFrame/Series to be compared to `expected`.
#'
#' @return A TRUE if equal, FALSE otherwise
#' @export
#' @examples
#' # ADD_EXAMPLES_HERE
check_values <- function(object = .result, expected = .solution, env = parent.frame()) {
  if (inherits(object, ".result")) {
    object <- get(".result", env)
  }
  if (inherits(expected, ".solution")) {
    expected <- get(".solution", env)
  }
  obj_vals <- translate(get_values(object))
  exp_vals <- translate(get_values(expected))
  identical(obj_vals, exp_vals)
}

#' Checks that two DataFrame/Series are the same.
#'
#' This will do the following checks:
#' 1. Check that the Index are equal
#' 2. Check that the columns are equal
#' 3. Check that the values are equal
#'
#' @param object A DataFrame/Series to be compared to `expected`.
#' @param expected The expected DataFrame/Series.
#'
#' @return A TRUE if equal, FALSE otherwise
#' @export
#' @examples
#' reticulate::py_run_string('import pandas as pd; import numpy as np')
#' .result <- reticulate::py_eval("pd.DataFrame({'a':[1,2,3]})")
#' .solution <- reticulate::py_eval("pd.DataFrame({'a':[1,2]})")
#' check_py_dataframe()
#'
#' .result <- reticulate::py_eval("pd.DataFrame({'a':[1,2,3]})")
#' .solution <- reticulate::py_eval("pd.DataFrame({'b':[1,2,3]})")
#' check_py_dataframe()
#' 
#' # TODO add a MultIindex column example as well
check_py_dataframe <- function(object = .result, expected = .solution, env = parent.frame()) {
  if (inherits(object, ".result")) {
    object <- get(".result", env)
  }
  if (inherits(expected, ".solution")) {
    expected <- get(".solution", env)
  }
  is_tbl <- tryCatch({
      object <- py_to_tbl(object)
      expected <- py_to_tbl(expected)
      TRUE
    }, error = function(e) {
      FALSE
    }
  )
  if (is_tbl) {
    tblcheck::tbl_check(object, expected, env = env)
  } else {
    return(
      check_index(object, expected) &&
      check_columns(object, expected) &&
      check_values(object, expected)
    )
  }
}
