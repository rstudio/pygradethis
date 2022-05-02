
#' R wrapper around `python_grade_learnr`
#'
#' To enable exercise checking in your learnr tutorial, you can set
#' `tutorial_options(exercise.checker = gradethispython::exercise_checker)` in the setup chunk
#' of your tutorial. Or, set the `exercise.checker` for an individual Python chunk.
#'
#' @param label Label for exercise chunk
#' @param solution_code Code provided within the “-solution” chunk for the
#'   exercise.
#' @param user_code Python code submitted by the user
#' @param check_code Code provided within the “-check” chunk for the exercise.
#' @param envir_result The Python environment after the execution of the chunk.
#' @param evaluate_result The return value from the `evaluate::evaluate`
#'   function.
#' @param envir_prep A copy of the Python environment before the execution of the
#'   chunk.
#' @param last_value The last value from evaluating the exercise.
#' @param ... Extra arguments supplied by learnr
#'
#' @return The `gradethis::graded()` list which contains several fields indicating the result of the
#'   check.
#' @export
exercise_checker <- function(label = NULL,
                            solution_code = NULL,
                            user_code = NULL,
                            check_code = NULL,
                            envir_result = NULL,
                            evaluate_result = NULL,
                            envir_prep = NULL,
                            last_value = NULL,
                            ...) {
  # need to cast environment types to a list so reticulate can translate to Python's dicts
  grade <- python_grade_learnr(
    label,
    solution_code,
    user_code,
    check_code,
    as.list(envir_result),
    evaluate_result,
    as.list(envir_prep),
    last_value
  )
  # Note: each field needs to be manually converted as the returned dict
  # cannot be converted properly as it gets interpreted as an environment
  structure(
    list(
      message = reticulate::py_to_r(grade$message),
      correct = reticulate::py_to_r(grade$correct),
      type = reticulate::py_to_r(grade$type),
      location = reticulate::py_to_r(grade$location)
    ),
    class = "gradethis_graded"
  )
}
