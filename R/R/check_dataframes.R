#' Get the Python result
#'
#' @param object The .result object.
#' @param env The environment to look for the .result.
#' @return A Python object
#' @keywords internal
get_python_result <- function(object = .result, env = parent.frame()) {
  if (inherits(object, ".result")) {
    object <- get(".result", env)
  }
  get0(".py_result", envir = env, ifnotfound = object)
}

#' Get the Python solution
#'
#' @param expected The .solution object.
#' @param env The environment to look for the .solution.
#' @return A Python object
#' @keywords internal
get_python_solution <- function(expected = .solution, env = parent.frame()) {
  if (inherits(expected, ".solution")) {
    expected <- get(".solution", env)
  }
  get0(".py_solution", envir = env, ifnotfound = expected)
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
#' pygradethis::py_get_index(.result)
#'
#' # RangeIndex(start=0, stop=3, step=1)
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
#' pygradethis::py_get_columns(.result)
#'
#' # Index(['a'], dtype='object')
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
#' pygradethis::py_get_values(.result)
#'
#' #      [,1]
#' # [1,]    1
#' # [2,]    2
#' # [3,]    3
#' }
py_get_values <- function(data) {
  data$values
}

#' Check and return a problem if the object is not the expected type
#'
#' This function is useful for any py_check_*() functions to validate
#' the object before moving on to grading.
#'
#' @param object any Python or R object.
#' @param expected_type A `character` for the class name (e.g. 'DataFrame')
#' @param problem_type A `character` for the problem to generate (e.g. 'wrong_index')
#'
#' @return a `NULL` if no problem, else a `pygradethis::problem`
#' @noRd
py_return_if_not_type <- function(object, expected_type, problem_type) {
  object_type <-
    if (is_py_object(object)) {
      pygradethis::get_friendly_class(object)
    } else {
      # when possible, we convert the student's object which goes through
      # `pygradethis::py_to_r` where we already set the appropriate class name
      # dispatched via the S4 generic for the particular type (see py_friendly_class.R)
      class(object)
    }

  # if there is a difference of type return a problem
  if (!identical(object_type, expected_type)) {
    extra <- NULL
    if (identical(object_type, "None")) {
      extra <- "Did you forget to return something?"
    }
    return(problem(
        type = problem_type,
        message = glue::glue(
          "I expected a {expected_type}, but your code returned a `{object_type}`. {extra}", .null = ""
        )
    ))
  }

  NULL
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
#' pygradethis::py_check_index()
#'
#' # $type
#' # [1] "wrong_index"
#' #
#' # $expected
#' # [1] 0 1 2
#' #
#' # $actual
#' # [1] 0 1
#' #
#' # $message
#' # [1] "The index does not match the expected."
#' #
#' # attr(,"class")
#' # [1] "wrong_index_problem" "pygradethis_problem" "gradethis_problem"
#' }
py_check_index <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  object <- get_python_result(object, env)
  expected <- get_python_solution(expected, env)

  left_vals <- NULL
  right_vals <- NULL

  # return if the object is not a DataFrame
  return_if_problem(
    py_return_if_not_type(object, "DataFrame", "wrong_index")
  )

  # validate input types / catch any errors to get values
  return_if_internal_problem({
    if (!pygradethis::is_DataFrame(expected)) {
      stop("The expected object must be of type `DataFrame`")
    }
    left_vals <- py_to_r(py_get_index(object))
    right_vals <- py_to_r(py_get_index(expected))
  })

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
#' .result <- reticulate::py_eval("pd.DataFrame({'a':[1, 2]})")
#' .solution <- reticulate::py_eval("pd.DataFrame({'a':[1, 2, 3]})")
#' py_grade_index()
#'
#' # <gradethis_graded: [Incorrect]
#' # The index does not match the expected. Your result should contain 3
#' # values, but it has 2 values. I expected your result to include the
#' # value `2`.
#' }
py_grade_index <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  object <- get_python_result(object, env)
  expected <- get_python_solution(expected, env)

  # find problems with index
  problem <- py_check_index(object, expected)

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
#' pygradethis::py_check_columns()
#'
#' # $type
#' # [1] "wrong_columns"
#' #
#' # $expected
#' # [1] "b"
#' #
#' # $actual
#' # [1] "a"
#' #
#' # $message
#' # [1] "The column names do not match the expected columns."
#' #
#' # attr(,"class")
#' # [1] "wrong_columns_problem" "pygradethis_problem"   "gradethis_problem"
#' }
py_check_columns <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  object <- get_python_result(object, env)
  expected <- get_python_solution(expected, env)

  obj_vals <- NULL
  exp_vals <- NULL

  # return if the object is not a DataFrame
  return_if_problem(
    py_return_if_not_type(object, "DataFrame", "wrong_columns")
  )

  # validate input types / catch any errors to get values
  return_if_internal_problem({
    if (!pygradethis::is_DataFrame(expected)) {
      stop("The expected object must be of type `DataFrame`")
    }
    obj_vals <- py_to_r(py_get_columns(object))
    exp_vals <- py_to_r(py_get_columns(expected))
  })

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
#' pygradethis::py_grade_columns()
#'
#' # <gradethis_graded: [Incorrect]
#' # The column names do not match the expected columns. The first value
#' # of your result should be `b`, not `a`.
#' # }
py_grade_columns <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  object <- get_python_result(object, env)
  expected <- get_python_solution(expected, env)

  # find problems with column names
  problem <- py_check_columns(object, expected)

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
#' pygradethis::py_check_values()
#'
#' # $type
#' # [1] "wrong_values"
#' #
#' # $expected
#' #      [,1]
#' # [1,]    1
#' # [2,]    2
#' # [3,]    3
#' #
#' # $actual
#' #      [,1]
#' # [1,]    1
#' # [2,]    2
#' # [3,]   99
#' #
#' # $message
#' # [1] "The DataFrame values do not match the expected values."
#' #
#' # attr(,"class")
#' # [1] "wrong_values_problem" "pygradethis_problem"  "gradethis_problem"
#' }
py_check_values <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  object <- get_python_result(object, env)
  expected <- get_python_solution(expected, env)

  obj_vals <- NULL
  exp_vals <- NULL

  # return if the object is not a DataFrame
  return_if_problem(
    py_return_if_not_type(object, "DataFrame", "wrong_values")
  )

  # validate expected input types
  return_if_internal_problem({
    if (!pygradethis::is_DataFrame(expected)) {
      stop("The expected object must be of type `DataFrame`")
    }
    obj_vals <- py_to_r(py_get_values(object))
    exp_vals <- py_to_r(py_get_values(expected))
  })

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
#' pygradethis::py_grade_values()
#'
#' # <gradethis_graded: [Incorrect]
#' # The DataFrame values do not match the expected values. The first 3
#' # values of your result should be `1`, `2`, and `3`, not `1`, `2`, and
#' # `99`.
#' }
py_grade_values <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  object <- get_python_result(object, env)
  expected <- get_python_solution(expected, env)

  # find problems with values
  problem <- py_check_values(object, expected)

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
#' pygradethis::py_check_series()
#'
#' # $type
#' # [1] "wrong_series"
#' #
#' # $expected
#' # 0 1 2
#' # 1 2 3
#' #
#' # $actual
#' # 0 1
#' # 1 2
#' #
#' # $message
#' # [1] "The Series do not match the expected Series."
#' #
#' # attr(,"class")
#' # [1] "wrong_series_problem" "pygradethis_problem"  "gradethis_problem"
#'
#' # Series w/ Index
#' .result = reticulate::py_eval("pd.Series(data={'a': 1, 'b': 2, 'd': 3})", F)
#' .solution =  reticulate::py_eval("pd.Series(data={'a': 1, 'b': 2, 'c': 3})", F)
#' pygradethis::py_check_series()
#'
#' # $type
#' # [1] "wrong_series"
#' #
#' # $expected
#' # a b c
#' # 1 2 3
#' #
#' # $actual
#' # a b d
#' # 1 2 3
#' #
#' # $message
#' # [1] "The Series do not match the expected Series."
#' #
#' # attr(,"class")
#' # [1] "wrong_series_problem" "pygradethis_problem"  "gradethis_problem"
#' }
py_check_series <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  object <- get_python_result(object, env)
  expected <- get_python_solution(expected, env)

  # return if the object is not a Series
  return_if_problem(
    py_return_if_not_type(object, "Series", "wrong_series")
  )

  # validate expected input type
  return_if_internal_problem({
    # NOTE: to not break things much, we're using `stop()` instead of `checkmate::assert`
    # we can use checkmate but changing is_Series() to throw an error when it's False
    # will break old grading code
    if (!pygradethis::is_Series(expected)) {
      stop("The expected object must be of type `Series`")
    }
  })

  if (is_py_object(object)) {
    object <- pygradethis::py_to_r(object)
  }
  if (is_py_object(expected)) {
    expected <- pygradethis::py_to_r(expected)
  }

  if (!identical(object, expected)) {
    return(problem(
      type = "wrong_series",
      message = "The Series does not match the expected Series.",
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
#' pygradethis::py_grade_series()
#'
#' # <gradethis_graded: [Incorrect]
#' # The Series do not match the expected Series. Your result should
#' # contain 3 values, but it has 2 values. I expected your result to
#' # include the value `3`.
#' }
py_grade_series <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  object <- get_python_result(object, env)
  expected <- get_python_solution(expected, env)

  # find problems with a Series
  problem <- py_check_series(object, expected)

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
#' @param env The environment used for grading.
#'
#' @return A NULL if equal, otherwise a `gradethis_graded` or `problem` object
#' @export
py_check_dataframe <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  object <- get_python_result(object, env)
  expected <- get_python_solution(expected, env)

  # validate expected input types
  return_if_internal_problem({
    if (!pygradethis::is_DataFrame(expected)) {
      stop("The expected object must be of type `DataFrame`")
    }
  })

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

  return_if_problem(py_check_index(object, expected))
  return_if_problem(py_check_columns(object, expected))
  return_if_problem(py_check_values(object, expected))

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
#' pygradethis::py_grade_dataframe()
#'
#' # <gradethis_graded: [Incorrect]
#' # The DataFrame values do not match the expected values. The first 3
#' # values of your result should be `1`, `2`, and `3`, not `1`, `2`, and
#' # `99`.
#' }
py_grade_dataframe <- function(
  object = .result, expected = .solution, env = parent.frame()
) {
  object <- get_python_result(object, env)
  expected <- get_python_solution(expected, env)

  # check for any dataframe problems
  problem <- py_check_dataframe(object, expected)

  if (!is_pygradethis_problem(problem) && !tblcheck::is_tblcheck_problem(problem)) {
    return(invisible())
  }

  tblcheck::problem_grade(problem)
}
