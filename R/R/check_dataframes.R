#' Get the Python result
#'
#' @param object The .result object.
#' @param env The environment to look for the .result.
#'
#' @noRd
#' @keywords internal
get_python_result <- function(object = .result, env = parent.frame()) {
  if (inherits(object, ".result")) {
    result <- get(".result", env)
    if (!is_py_object(result)) {
      return(get0(
        ".py_result",
        envir = env,
        ifnotfound = result
      ))
    }
  }
  object
}

#' Get the Python solution
#'
#' @param object The .solution object.
#' @param env The environment to look for the .solution.
#'
#' @noRd
#' @keywords internal
get_python_solution <- function(object = .solution, env = parent.frame()) {
  if (inherits(object, ".solution")) {
    solution <- get(".solution", env)
    if (!is_py_object(solution)) {
      return(get0(
        ".py_solution",
        envir = env,
        ifnotfound = solution
      ))
    }
  }
  object
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
  object <- get_python_result(object, env)
  expected <- get_python_solution(expected, env)

  left_vals <- py_to_r(py_get_index(object))
  right_vals <- py_to_r(py_get_index(expected))

  if (!identical(left_vals, right_vals)) {
    return(problem(
      type = "wrong_index",
      message = "The index does not match the expected.",
      actual = left_vals,
      expected = right_vals
    ))
  }
  NULL
}

#' Check the index of a DataFrame/Series matches the expected index,
#' and return a `gradethis::fail` if they don't.
#'
#' @param object A DataFrame/Series to be compared to `expected`.
#' @param expected A DataFrame/Series containing the expected index.
#' @param env The environment used for grading.
#'
#' @return A `gradethis::fail()` if the index does not match else NULL
#' @export
#' @examples
#' \dontrun{
#' reticulate::py_run_string('import pandas as pd; import numpy as np')
#' .result <- reticulate::py_eval("pd.DataFrame({'a':[1,2]})")
#' .solution <- reticulate::py_eval("pd.DataFrame({'a':[1,2,3]})")
#' py_grade_index() # a gradethis::fail()
#' }
py_grade_index <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  # find problems with index
  problem <- py_check_index(object, expected, env)

  if (!is_pygradethis_problem(problem)) {
    return(invisible())
  }

  tblcheck::problem_grade(problem)
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
  object <- get_python_result(object, env)
  expected <- get_python_solution(expected, env)

  # extract column values
  obj_vals <- py_to_r(py_get_columns(object))
  exp_vals <- py_to_r(py_get_columns(expected))

  if (!identical(obj_vals, exp_vals)) {
    return(problem(
      type = "wrong_columns",
      message = "The column names do not match the expected columns.",
      actual = obj_vals,
      expected = exp_vals
    ))
  }

  NULL
}

#' Checks that the columns of two DataFrame/Series are the same and returns
#' a `gradethis::fail` if they don't.
#'
#' @param object A DataFrame to be compared to `expected`.
#' @param expected A DataFrame containing the expected column.
#' @param env The environment used for grading.
#'
#' @return A `gradethis::fail()` if the index does not match else NULL
#' @export
#' @examples
#' \dontrun{
#' reticulate::py_run_string('import pandas as pd; import numpy as np')
#' .result <- reticulate::py_eval("pd.DataFrame({'a':[1,2,3]})")
#' .solution <- reticulate::py_eval("pd.DataFrame({'b':[1,2,3]})")
#' py_grade_columns() # a gradethis::fail()
#' }
py_grade_columns <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  # find problems with column names
  problem <- py_check_columns(object, expected, env)

  if (!is_pygradethis_problem(problem)) {
    return(invisible())
  }

  tblcheck::problem_grade(problem)
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
  object <- get_python_result(object, env)
  expected <- get_python_solution(expected, env)

  obj_vals <- py_to_r(py_get_values(object))
  exp_vals <- py_to_r(py_get_values(expected))

  if (!identical(obj_vals, exp_vals)) {
    return(problem(
      type = "wrong_values",
      message = "The DataFrame values do not match the expected values.",
      actual = obj_vals,
      expected = exp_vals
    ))
  }
  NULL
}

#' Checks that the values of two DataFrame/Series are the same and returns
#' a `gradethis::fail` if they don't.
#'
#' @param object A DataFrame to be compared to `expected`.
#' @param expected A DataFrame containing the expected values.
#' @param env The environment used for grading.
#'
#' @return A `gradethis::fail()` if the index does not match else NULL
#' @export
#' @examples
#' \dontrun{
#' reticulate::py_run_string('import pandas as pd; import numpy as np')
#' .result <- reticulate::py_eval("pd.DataFrame({'a':[1,2,99]})")
#' .solution <- reticulate::py_eval("pd.DataFrame({'a':[1,2,3]})")
#' py_grade_values() # a gradethis::fail()
#' }
py_grade_values <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  # find problems with values
  problem <- py_check_values(object, expected, env)

  if (!is_pygradethis_problem(problem)) {
    return(invisible())
  }

  tblcheck::problem_grade(problem)
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
  object <- get_python_result(object, env)
  expected <- get_python_solution(expected, env)

  if (is_py_object(object)) {
    object <- pygradethis::py_to_r(object)
  }
  if (is_py_object(expected)) {
    expected <- pygradethis::py_to_r(expected)
  }

  if (!identical(object, expected)) {
    return(problem(
      type = "wrong_series",
      message = "The Series do not match the expected Series.",
      actual = object,
      expected = expected
    ))
  }
  NULL
}

#' Checks that two Series are the same and returns
#' a `gradethis::fail` if they don't.
#'
#' @param object A Series to be compared to `expected`.
#' @param expected The expected Series
#' @param env The environment used for grading.
#'
#' @return A `gradethis::fail()` if the index does not match else NULL
#' @export
#' @examples
#' \dontrun{
#' reticulate::py_run_string('import pandas as pd; import numpy as np')
#' .result = reticulate::py_eval("pd.Series(data=[1, 2])", F)
#' .solution = reticulate::py_eval("pd.Series(data=[1, 2, 3])", F)
#' py_grade_series() # a gradethis::fail()
#' }
py_grade_series <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  # find problems with a Series
  problem <- py_check_series(object, expected, env)

  if (!is_pygradethis_problem(problem)) {
    return(invisible())
  }

  tblcheck::problem_grade(problem)
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
  object <- get_python_result(object, env)
  expected <- get_python_solution(expected, env)

  if (is_py_object(object)) {
    object <- pygradethis::py_to_r(object)
  }
  if (is_py_object(expected)) {
    expected <- pygradethis::py_to_r(expected)
  }

  # if result and solution are already converted use tblcheck
  if (!is_py_object(object) && !is_py_object(expected)) {
    return(tblcheck::tbl_check(object, expected, env = env))
  }

  return_if_problem(py_check_index(object, expected), env)
  return_if_problem(py_check_columns(object, expected), env)
  return_if_problem(py_check_values(object, expected), env)

  NULL
}

#' Checks that two DataFrame are the same and returns
#' a `gradethis::fail` if they don't.
#'
#' @param object A DataFrame to be compared to `expected`.
#' @param expected The expected DataFrame
#' @param env The environment used for grading.
#'
#' @return A `gradethis::fail()` if the index does not match else NULL
#' @export
#' @examples
#' \dontrun{
#' reticulate::py_run_string('import pandas as pd; import numpy as np')
#' .result <- reticulate::py_eval("pd.DataFrame({'a':[1,2,99]})")
#' .solution <- reticulate::py_eval("pd.DataFrame({'a':[1,2,3]})")
#' py_grade_dataframe() # a gradethis::fail()
#' }
py_grade_dataframe <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  object <- get_python_result(object, env)
  expected <- get_python_solution(expected, env)

  # if result and solution are already converted use tblcheck
  use_tblcheck <- !is_py_object(object) && !is_py_object(expected)
  if (use_tblcheck) {
    return(tblcheck::tbl_grade(object, expected, env = env))
  }

  # otherwise, grade using the raw Python result and solution
  py_grade_index(object, expected)
  py_grade_columns(object, expected)
  py_grade_values(object, expected)
}
