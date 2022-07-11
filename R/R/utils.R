
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

# helper function that converts a Python DataFrame ensuring that
# the Index/MultiIndex is flattened 
convert_to_tbl <- function(data) {
  data_reset <- data$reset_index()
  # attempt to convert directly to tibble
  tbl <- tryCatch(tibble::as_tibble(data_reset), error = function(e) NULL)
  if (is.null(tbl)) {
    # if conversion to tibble fails, first convert to R data.frame
    tbl <- tibble::as_tibble(reticulate::py_to_r(data_reset))
  }
  # for regular dataframes we will end up with an "index" column
  # so we remove that
  if ("index" %in% names(tbl)) {
    return(dplyr::select(tbl, -index))
  } else {
    return(tbl)
  }
}

#' Converts a Python pandas.DataFrame into an R tibble
#'
#' @param data A pandas.DataFrame
#'
#' @return A tibble
#' @export
py_to_tbl <- function(data) {
  # check if data is a MultiIndex (e.g. multiple groups)
  if ("pandas.core.indexes.multi.MultiIndex" %in% class(data$index)) {
    py_run_string("import builtins")
    # NOTE: the index names is a FrozenList so we have to cast it with list()
    # flatten MultiIndex into regular columns
    group_vars <- py$builtins$list(data$index$names)
    tbl <- convert_to_tbl(data)
    # construct a tibble and apply any groups
    return(dplyr::group_by(tbl, dplyr::across(group_vars)))
  }
  # reset Index for DataFrames that have rownames
  convert_to_tbl(data)
}
