
#' R wrapper around `pygradethis_exercise_checker`
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
exercise_checker <- function(
  label = NULL,
  solution_code = NULL,
  user_code = NULL,
  check_code = NULL,
  envir_result = NULL,
  evaluate_result = NULL,
  envir_prep = NULL,
  last_value = NULL,
  ...
) {
  # retrieve the Python environment from the envir_prep / envir_result
  envir_prep_py <- get0(".__py__", envir = envir_prep, ifnotfound = NULL)
  envir_result_py <- get0(".__py__", envir = envir_result, ifnotfound = NULL)
  # get solution object for result checking
  .solution <- tryCatch({
      solution_code <- paste0(as.character(solution_code), collapse = "\n")
      get_last_value(solution_code, envir_prep_py)
    },
    error = function(e) {
      NULL
    }
  )
  # redirect table grading to tblcheck for now if solution object is a DataFrame
  if (!is.null(.solution) && class(.solution) %in% "pandas.core.frame.DataFrame") {
    # auto convert the result and solution to a tibble before the tblcheck grading
    # (we can also choose to not convert here and let user do conversions)
    .result <- py_to_tbl(last_value)
    .solution <- py_to_tbl(.solution)
    # prep the checking environment
    checking_env <-
      list2env(list(
        .solution = .solution,
        .envir_prep = envir_prep,
        .envir_result = envir_result,
        .last_value = .result,
        .result = .result,
        .user = .result
    ))
    # grade
    checker_fun <- eval(parse(text = check_code))
    return(checker_fun(checking_env))
  }

  # if not a DataFrame, use assert checking to produce a grade result
  grade <- pygradethis_exercise_checker(
    label,
    solution_code,
    user_code,
    check_code,
    envir_result_py,
    evaluate_result,
    envir_prep_py,
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

#' A shim around the `gradethis::py_gradethis_exercise_checker` for grading Python exercises.
#'
#' To enable exercise checking in your learnr tutorial through R code (i.e. an R -check chunk), 
#' you can set `tutorial_options(exercise.checker = pygradethis::py_gradethis_exercise_checker)` 
#' in the setup chunk of your tutorial. Or, set the `exercise.checker` for an individual Python chunk.
#'
#' @param label Label for exercise chunk
#' @param solution_code Code provided within the “-solution” chunk for the
#'   exercise.
#' @param user_code Python code submitted by the user
#' @param check_code Code provided within the “-check” chunk for the exercise.
#' @param envir_result The R environment after the execution of the chunk
#'   which also contains a Python main module environment
#' @param evaluate_result The return value from the `evaluate::evaluate`
#'   function.
#' @param envir_prep A copy of the R environment before the execution of the
#'   chunk which also contains a Python main module environment.
#' @param last_value The last value from evaluating the exercise.
#' @param ... Extra arguments supplied by learnr
#'
#' @return The `gradethis::graded()` list which contains several fields indicating the 
#' result of the check.
#' @export
py_gradethis_exercise_checker <- function(
  label = NULL,
  solution_code = NULL,
  user_code = NULL,
  check_code = NULL,
  envir_result = NULL,
  evaluate_result = NULL,
  envir_prep = NULL,
  last_value = NULL,
  ...
) {
  withr::local_options(list(
    gradethis.exercise_checker.solution_eval_fn = list(
      python = function(code, envir) {
        pygradethis:::return_if_internal_problem({
          envir_prep_py <- get0(".__py__", envir = envir, ifnotfound = NULL)
          solution_code <- paste0(as.character(solution_code), collapse = "\n")
          solution <- pygradethis::get_last_value(solution_code, envir_prep_py)
          # keep around raw Python solution object in case it's needed
          assign(".py_solution", solution, envir = envir)
          pygradethis::py_to_r(solution)
        })
      }
    )
  ))
  # keep around raw Python environment and result in case we need them
  py_envir_result <- get0(".__py__", envir = envir_result, ifnotfound = NULL)
  py_result <- last_value
  # convert the result and Python environment to R
  last_value <- pygradethis::py_to_r(last_value)
  envir_result <- pygradethis::get_py_envir(py_envir_result)
  # use `gradethis::gradethis_exercise_checker` with the custom solution(s) evaluator
  gradethis::gradethis_exercise_checker(
    label = label,
    solution_code = solution_code,
    user_code = user_code,
    check_code = check_code,
    envir_result = envir_result,
    evaluate_result = evaluate_result,
    envir_prep = envir_prep,
    last_value = last_value,
    py_result = py_result,
    py_envir_result = py_envir_result,
    ...
  )
}
