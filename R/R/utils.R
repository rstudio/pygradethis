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

is.DataFrame <- function(obj) {
  reticulate::py$builtins$isinstance(obj, reticulate::py$pd$DataFrame)
}

is.Index <- function(obj) {
  reticulate::py$builtins$isinstance(obj, reticulate::py$pd$Index)
}

is.RangeIndex <- function(obj) {
  reticulate::py$builtins$isinstance(obj, reticulate::py$pd$RangeIndex)
}

is.CategoricalIndex <- function(obj) {
  reticulate::py$builtins$isinstance(obj, reticulate::py$pd$CategoricalIndex)
}

is.MultiIndex <- function(obj) {
  reticulate::py$builtins$isinstance(obj, reticulate::py$pd$MultiIndex)
}

is.np.array <- function(obj) {
  reticulate::py$builtins$isinstance(obj, reticulate::py$np$array)
}

# 
# If the object can't be converted we return the Python object as-is

#' Wrapper of reticulate::py_to_r to translate objects from Python to R.
#'
#' @param obj A Python object.
#'
#' @return An R object, or Python object if we can't translate
#' @export
translate <- function(obj) {
  return(
    tryCatch({
      if (is.DataFrame(obj)) {
        # for a DataFrame try to convert to a tibble for tblcheck grading
        return(py_to_tbl(obj))
      } else if (is.MultiIndex(obj)) {
        # MultiIndex -> np.array -> list(list())
        return(reticulate::py_to_r(obj$values$tolist()))
      } else if (is.Index(obj)) {
        if (is.CategoricalIndex(obj)) {
          # CategoricalIndex -> np.array -> list
          return(reticulate::py_to_r(obj$values$tolist()))
        } else if (is.RangeIndex(obj) || is.np.array(obj)) {
          # <>.Index -> list
          return(obj$values)
        }
      } else {
        return(reticulate::py_to_r(obj))
      }
    }, error = function(e) {
      # if anything fails above, just return the Python object
      obj
    }
    )
  )
}

# helper function that flattens a Python DataFrame ensuring that
# the Index/MultiIndex is flattened and converted to columns
flatten_py_dataframe <- function(data) {
  # flatten the row Index
  data <- data$reset_index()
  # convert to tible
  tbl <- tryCatch(
    tibble::as_tibble(data),
    error = function(e) {
      # if conversion to tibble fails, first convert to R data.frame
      tibble::as_tibble(reticulate::py_to_r(data))
    }
  )
  # for a regular DataFrame we will end up with an "index" column
  # so we remove that
  if ("index" %in% names(tbl)) {
    tbl <- dplyr::select(tbl, -index)
  }
  # set the base class
  class(tbl) <- append("py_tbl_df", class(tbl))
  # NOTE: "pandas.index" will have a pointer address that will be unique so
  # comparing identical tibbles won't work unless this is stripped off
  attr(tbl, "pandas.index") <- NULL
  tbl
}

#' Converts a Python pandas.DataFrame into an R tibble
#'
#' @param data A pandas.DataFrame
#'
#' @return A tibble
#' @export
py_to_tbl <- function(data) {
  if (!any(class(data) %in% "pandas.core.frame.DataFrame")) {
    # assign Python type to the object's class
    obj_class <- reticulate::py$builtins$type(data)$`__name__`
    data <- reticulate::py_to_r(data)
    class(data) <- obj_class
    return(data)
  }
  reticulate::py_run_string("import builtins", convert = FALSE)
  # check if data should be grouped
  index_names <- reticulate::py$builtins$list(data$index$names)
  has_groups <- all(vapply(index_names, Negate(is.null), logical(1)))
  # flatten Index/MultiIndex
  tbl <- flatten_py_dataframe(data)
  # construct a tibble that has groups if needed
  if (has_groups) {
    # NOTE: the index names is a FrozenList so we have to cast it with list()
    # flatten MultiIndex into regular columns
    group_vars <- reticulate::py$builtins$list(data$index$names)
    if (length(group_vars) > 0) {
      tbl <- dplyr::group_by(tbl, dplyr::across(group_vars))
    }
    class(tbl) <- append(c("py_grouped_df", "py_tbl_df"), class(tbl))
    return(tbl)
  }
  tbl
}
