

#' Helper function to return early from `py_check_*` functions
#'
#' This is especially useful when returning from checking functions that
#' combine multiple checks
#'
#' @param problem A `pygradethis_problem` object.
#' @param env The environment from which to return.
#'
#' @keywords internal
#' @noRd
return_if_problem <- function(problem, env = parent.frame()) {
  if (is_pygradethis_problem(problem)) {
    rlang::return_from(env, problem)
  }
  NULL
}

#' Declare a problem
#'
#' Useful for constructing a small list to communicate the problem that was
#' discovered during checking.
#'
#' @param type A character string, e.g. `columns`, `index`, or `values` that
#'   describes the problem that was discovered.
#' @param expected actual The expected and actual values. These should be
#'   included when the value is a summary, e.g. `nrow(expected)` or
#'   `length(actual)`. Be careful not to include large amounts of data.
#' @param ... Additional elements to be included in the `problem` object.
#'
#' @keywords internal
#' @noRd
problem <- function(
  type, expected = NULL, actual = NULL, correct = FALSE, ...
) {
  checkmate::assert_string(type, min.chars = 1)

  problem <- list(
    type = type,
    correct = correct,
    expected = expected,
    actual = actual,
    ...
  )

  structure(
    purrr::compact(problem),
    class = c(paste0(type, "_problem"), "pygradethis_problem", "gradethis_problem")
  )
}

is_pygradethis_problem <- function(x, type = NULL) {
  inherits(x, "pygradethis_problem") &&
  (is.null(type) || inherits(x, paste0(type, "_problem")))
}

#' Get the index of a pandas.DataFrame/pandas.Series
#'
#' @param data A DataFrame/Series.
#'
#' @return An Index/MultiIndex
#' @export
#' @examples
#' \dontrun{
#' reticulate::py_run_string('import pandas as pd; import numpy as np')
#' .result <- reticulate::py_eval("pd.DataFrame({'a':[1,2,3]})")
#' py_get_index(.result) # RangeIndex(start=0, stop=3, step=1)
#' }
py_get_index <- function(data) {
  data$index
}

#' Get the columns of a pandas.DataFrame/pandas.Series
#'
#' @param data A DataFrame/Series.
#'
#' @return An Index/MultiIndex
#' @export
#' @examples
#' \dontrun{
#' reticulate::py_run_string('import pandas as pd; import numpy as np')
#' .result <- reticulate::py_eval("pd.DataFrame({'a':[1,2,3]})")
#' py_get_columns(.result) # Index(['a'], dtype='object')
#' }
py_get_columns <- function(data) {
  data$columns
}

#' Get the values of a pandas.DataFrame/pandas.Series
#'
#' @param data A DataFrame/Series.
#'
#' @return An np.array of values
#' @export
#' @examples
#' \dontrun{
#' reticulate::py_run_string('import pandas as pd; import numpy as np')
#' .result <- reticulate::py_eval("pd.DataFrame({'a':[1,2,3]})")
#' py_get_values(.result)
#' #      [,1]
#' # [1,]    1
#' # [2,]    2
#' # [3,]    3
#' }
py_get_values <- function(data) {
  data$values
}

#' Checks that the Index of two DataFrame/Series are the same.
#'
#' Extracts the values out of the Index to do the check.
#'
#' @param object A DataFrame/Series to be compared to `expected`.
#' @param expected A DataFrame/Series containing the expected column.
#' @param env The environment used for grading.
#'
#' @return A NULL if equal, a `pygradethis_problem` object otherwise
#' @export
#' @examples
#' \dontrun{
#' reticulate::py_run_string('import pandas as pd; import numpy as np')
#' .result <- reticulate::py_eval("pd.DataFrame({'a':[1,2]})")
#' .solution <- reticulate::py_eval("pd.DataFrame({'a':[1,2,3]})")
#' py_check_index() # FALSE
#' }
py_check_index <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  if (inherits(object, ".result")) {
    object <- get(".result", env)
  }
  if (inherits(expected, ".solution")) {
    expected <- get(".solution", env)
  }
  left_vals <- py_to_r(py_get_index(object))
  right_vals <- py_to_r(py_get_index(expected))
  if (!identical(left_vals, right_vals)) {
    return(problem(
      type = "index",
      message = "The index does not match the expected.",
      actual = left_vals,
      expected = right_vals
    ))
  }
  NULL
}

#' Checks that the columns of two DataFrame/Series are the same.
#'
#' This extracts columns from the two objects, converts them to R lists
#' and checks that they are identical.
#'
#' @param object A DataFrame to be compared to `expected`.
#' @param expected A DataFrame containing the expected column.
#' @param env The environment used for grading.
#'
#' @return A NULL if equal, a `pygradethis_problem` object otherwise
#' @export
#' @examples
#' \dontrun{
#' reticulate::py_run_string('import pandas as pd; import numpy as np')
#' .result <- reticulate::py_eval("pd.DataFrame({'a':[1,2,3]})")
#' .solution <- reticulate::py_eval("pd.DataFrame({'b':[1,2,3]})")
#' py_check_columns() # FALSE
#' }
py_check_columns <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  if (inherits(object, ".result")) {
    object <- get(".result", env)
  }
  if (inherits(expected, ".solution")) {
    expected <- get(".solution", env)
  }
  # extract and py_to_r column values
  obj_vals <- py_to_r(py_get_columns(object))
  exp_vals <- py_to_r(py_get_columns(expected))
  if (!identical(obj_vals, exp_vals)) {
    return(problem(
      type = "columns",
      message = "The column names do not match the expected columns.",
      actual = obj_vals,
      expected = exp_vals
    ))
  }
  NULL
}

#' Checks that the values of two DataFrame/Series are the same.
#'
#' This extracts values from the two objects, converts them to R lists
#' and checks that they are identical.
#'
#' @param object A DataFrame/Series to be compared to `expected`.
#' @param expected The expected DataFrame/Series
#' @param env The environment used for grading.
#'
#' @return A NULL if equal, a `pygradethis_problem` object otherwise
#' @export
#' @examples
#' \dontrun{
#' reticulate::py_run_string('import pandas as pd; import numpy as np')
#' .result <- reticulate::py_eval("pd.DataFrame({'a':[1,2,99]})")
#' .solution <- reticulate::py_eval("pd.DataFrame({'a':[1,2,3]})")
#' py_check_values() # FALSE
#' }
py_check_values <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  if (inherits(object, ".result")) {
    object <- get(".result", env)
  }
  if (inherits(expected, ".solution")) {
    expected <- get(".solution", env)
  }
  obj_vals <- py_to_r(py_get_values(object))
  exp_vals <- py_to_r(py_get_values(expected))
  if (!identical(obj_vals, exp_vals)) {
    return(problem(
      type = "values",
      message = "The DataFrame values do not match the expected values.",
      actual = obj_vals,
      expected = exp_vals
    ))
  }
  NULL
}

#' Checks that two Series are the same.
#'
#' This checks both the names and the values are the same.
#'
#' @param object A Series to be compared to `expected`..
#' @param expected The expected Series.
#' @param env The environment used for grading.
#'
#' @return A NULL if equal, a `pygradethis_problem` object otherwise
#' @export
#' @examples
#' \dontrun{
#' reticulate::py_run_string('import pandas as pd; import numpy as np')
#' # Plain Series
#' .result = reticulate::py_eval("pd.Series(data=[1, 2])", F)
#' .solution = reticulate::py_eval("pd.Series(data=[1, 2, 3])", F)
#' py_check_series() # FALSE
#'
#' # Series w/ Index
#' .result = reticulate::py_eval("pd.Series(data={'a': 1, 'b': 2, 'd': 3})", F)
#' .solution =  reticulate::py_eval("pd.Series(data={'a': 1, 'b': 2, 'c': 3})", F)
#' py_check_series() # FALSE
#' }
py_check_series <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  if (inherits(object, ".result")) {
    object <- get(".result", env)
  }
  if (inherits(expected, ".solution")) {
    expected <- get(".solution", env)
  }
  obj_vector <- py_to_r(object)
  sol_vector <- py_to_r(expected)
  if (!identical(obj_vector, sol_vector)) {
    return(problem(
      type = "series",
      message = "The Series do not match the expected Series.",
      actual = obj_vector,
      expected = sol_vector
    ))
  }
  NULL
}

#' Checks that two DataFrame are the same.
#'
#' If DataFrames are tibble-able, rely on tblcheck::tbl_check() feedback
#'
#' Otherwise the following checks are performed:
#' 1. Check that the Index are equal (see `pygradethis::py_check_index()`)
#' 2. Check that the columns are equal (see `pygradethis::py_check_columns()`)
#' 3. Check that the values are equal (see `pygradethis::py_check_values()`)
#'
#' @param object A DataFrame to be compared to `expected`.
#' @param expected The expected DataFrame.
#'
#' @return A NULL if equal, otherwise a `gradethis_graded` or `problem` object
#' @export
py_check_dataframe <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
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
    return(tblcheck::tbl_grade(object, expected, env = env))
  } else {
    return_if_problem(py_check_index(object, expected), env)
    return_if_problem(py_check_columns(object, expected), env)
    return_if_problem(py_check_values(object, expected), env)
  }
  NULL
}
