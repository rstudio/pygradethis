# Mocking functions ----

#' A helper function to mock a Python exercise in learnr.
#'
#' This is an internal function used for testing purposes.
#'
#' @param user_code Python code submitted by the user
#' @param solution_code Code provided within the "-solution" chunk for the
#'   exercise.
#' @param check Code provided within the "-check" chunk for the exercise.
#' @param ... Extra grading arguments
#'
#' @return The mocked exercise
mock_py_exercise <- function(user_code, solution_code, check, ...) {
  # TODO: this currently will not work for the tblcheck grading of Python dataframes.
  learnr:::mock_exercise(
    user_code = user_code,
    solution_code = solution_code,
    engine = "python",
    check = check,
    # NOTE: we might want to make this a parameter as well to swap gradethis shim for testing
    exercise.checker = learnr:::dput_to_string(pygradethis::exercise_checker),
    ...
  )
}

#' A helper function to test evaluation of a mocked Python exercise through learnr
#'
#' This is an internal function used for testing purposes.
#'
#' @param ex A mocked Python exercise
#' @param envir An environment
#' @param evaluate_global_setup Whether to evaluate global setup code
#'
#' @return The feedback list
evaluate_exercise_feedback <- function(ex, envir = NULL, evaluate_global_setup = FALSE) {
  if (is.null(envir)) envir <- new.env()
  res <- learnr:::evaluate_exercise(ex, envir = envir, evaluate_global_setup = evaluate_global_setup)
  res$feedback
}

# Type checking helpers ----

#' Checks if the Python object is a pandas.DataFrame
#'
#' @param obj Python object.
#'
#' @return TRUE if so, FALSE otherwise
#' @export
is_DataFrame <- function(obj) {
  identical(get_friendly_class(obj), 'DataFrame')
}

#' Checks if the Python object is a pandas.Series
#'
#' @param obj Python object.
#'
#' @return TRUE if so, FALSE otherwise
#' @export
is_Series <- function(obj) {
  identical(get_friendly_class(obj), 'Series')
}

#' Checks if the Python object is a pandas.Index
#'
#' @param obj Python object.
#'
#' @return TRUE if so, FALSE otherwise
#' @export
is_Index <- function(obj) {
  identical(get_friendly_class(obj), 'Index')
}

#' Checks if the Python object is a function
#'
#' @param obj Python object.
#'
#' @return TRUE if so, FALSE otherwise
#' @export
is_RangeIndex <- function(obj) {
  identical(get_friendly_class(obj), 'RangeIndex')
}

#' Checks if the Python object is a pandas.CategoricalIndex
#'
#' @param obj Python object.
#'
#' @return TRUE if so, FALSE otherwise
#' @export
is_CategoricalIndex <- function(obj) {
  identical(get_friendly_class(obj), 'CategoricalIndex')
}

#' Checks if the Python object is a function
#'
#' @param obj Python object.
#'
#' @return TRUE if so, FALSE otherwise
#' @export
is_MultiIndex <- function(obj) {
  identical(get_friendly_class(obj), 'MultiIndex')
}

#' Checks if the Python object is a numpy.array
#'
#' @param obj Python object.
#'
#' @return TRUE if so, FALSE otherwise
#' @export
is_numpy_array <- function(obj) {
  identical(get_friendly_class(obj), 'array')
}


#' Checks if the Python object is a function
#'
#' @param obj Python object.
#'
#' @return TRUE if so, FALSE otherwise
#' @export
is_function <- function(obj) {
  identical(get_friendly_class(obj), 'function')
}

#' Get a friendly single string representation of a Python
#' object's class
#'
#' @param obj Python object.
#'
#' @return character
#' @export
get_friendly_class <- function(obj) {
  reticulate::py$builtins$type(obj)$`__name__`
}

# Python to R translation helpers ----

#' Wrapper of reticulate::py_to_r to convert objects from Python to R.
#'
#' `py_to_r` will attempt to reasonably convert objects that `reticulate::py_to_r` either can't
#' or when it produces a messy object (e.g. DataFrames with a MultiIndex)
#'
#' @param obj A Python object.
#'
#' @return An R object, or Python object if we can't py_to_r
#' @export
py_to_r <- function(obj) {
  return(
    tryCatch({
      py_obj <- NULL
      if (is_DataFrame(obj)) {
        # for a DataFrame try to convert to a tibble for tblcheck grading
        py_obj <- py_to_tbl(obj)
      } else if (is_Series(obj)) {
        py_obj <- reticulate::py_to_r(obj)
      } else if (is_MultiIndex(obj)) {
        py_obj <- index_to_list(obj)
      } else if (is_CategoricalIndex(obj)) {
        py_obj <- index_to_list(obj)
      } else if (is_Index(obj) || is_RangeIndex(obj)) {
        py_obj <- index_to_list(obj)
      } else {
        py_obj <- reticulate::py_to_r(obj)
        class(py_obj) <- get_friendly_class(obj)
      }
      return(py_obj)
    }, error = function(e) {
      # if anything fails above, just return the Python object
      obj
    }
    )
  )
}

#' Helper funtion to unpack an Index and return the values
#'
#' @param obj A type of Index
#'
#' @return A list()
index_to_list <- function(obj) {
  # if MultiIndex don't unlist
  if (pygradethis:::is_MultiIndex(obj)) {
    return(reticulate::py$builtins$list(obj))
  }
  # if CategoricalIndex, need to unpack the categories first
  if (pygradethis:::is_CategoricalIndex(obj)) {
    return(reticulate::py$builtins$list(obj$categories))
  }
  # unpack values
  # <>Index -> np.array -> list(list())
  unlist(reticulate::py$builtins$list(obj$values))
}

#' Converts a Python pandas.DataFrame into an R tibble
#'
#' @param data A pandas.DataFrame
#'
#' @return A tibble
#' @export
py_to_tbl <- function(data) {
  if (!is_DataFrame(data)) {
    # assign Python type to the object's class
    obj_class <- reticulate::py$builtins$type(data)$`__name__`
    data <- reticulate::py_to_r(data)
    class(data) <- obj_class
    return(data)
  }
  reticulate::py_run_string("import builtins", convert = FALSE)
  # flatten Index/MultiIndex
  flatten_py_dataframe(data)
}

# helper function that flattens a Python DataFrame ensuring that
# the Index/MultiIndex is flattened and converted to columns
flatten_py_dataframe <- function(data) {
  # do not handle dataframes that have MultiIndex columns
  if (is_MultiIndex(data$columns)) {
    return(data)
  }
  # flatten the row Index/MultiIndex as a result of a .groupby().agg()
  if (is_Index(data$index) || is_MultiIndex(data$index)) {
    # check if data should be grouped
    group_vars <- reticulate::py$builtins$list(data$index$names)
    has_groups <- all(vapply(group_vars, Negate(is.null), logical(1)))
    if (has_groups) {
      data <- data$reset_index()
      # convert to tibble
      tbl <- tibble::as_tibble(reticulate::py_to_r(data))
      tbl <- dplyr::group_by(tbl, dplyr::across(group_vars))
      class(tbl) <- append(c("py_grouped_df", "py_tbl_df"), class(tbl))
      attr(tbl, "pandas.index") <- NULL
      return(tbl)
    }
  }
  # otherwise just drop Index
  data <- data$reset_index(drop = TRUE)
  # convert to tibble
  tbl <- tibble::as_tibble(reticulate::py_to_r(data))
  # set the base class
  class(tbl) <- append("py_tbl_df", class(tbl))
  # NOTE: "pandas.index" will have a pointer address that will be unique so
  # comparing identical tibbles won't work unless this is stripped off
  attr(tbl, "pandas.index") <- NULL
  tbl
}

#' Convert variables within a Python module/environment.
#'
#' This takes in a Python dictionary representing the Python
#' environment, converts each object (if possible) and returns
#' a named list of R objects.
#'
#' @param envir A Python dictionary.
#'
#' @return A named list
#' @export
get_py_envir <- function(envir) {
  if (is.null(envir)) {
    return(envir)
  }
  Map(names(envir), f = function(obj_name) {
    pygradethis::py_to_r(envir[obj_name])
  })
}

# small helper function to determine if an object is a
# Python object or not
is_py_object <- function(obj) {
  tryCatch({
    reticulate::py_to_r(obj)
    TRUE
  }, error = function(e) {
    FALSE
  })
}

#' A wrapper around `identical()` to compare R objects that were
#' converted from Python.
#'
#' @param x any R object
#' @param y any R object
#'
#' @return TRUE/FALSE
#' @export
py_identical <- function(x, y) {
  identical(unclass(x), y)
}

# Misc ----

md_code <- function(x) {
  if (!length(x)) return(x)
  paste0("`", trimws(format(x, digits = 3)), "`")
}
