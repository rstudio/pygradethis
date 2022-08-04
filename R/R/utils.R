
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

# helper function that flattens a Python DataFrame ensuring that
# the Index/MultiIndex is flattened and converted to columns
flatten_py_dataframe <- function(data) {
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
  reticulate::py_run_string("import builtins")
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
