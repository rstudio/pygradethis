library(reticulate)

# helper function to test the exercise checker through the learnr flow
get_exercise_result <- function(user_code, solution_code, check_code, evaluate_global_setup = FALSE, ...) {
  ex <- learnr:::mock_exercise(
    user_code = user_code,
    solution_code = solution_code,
    engine = "python",
    check = check_code,
    exercise.checker = learnr:::dput_to_string(pygradethis::exercise_checker),
    ...
  )
  res <- learnr:::evaluate_exercise(ex, envir = new.env(), evaluate_global_setup = evaluate_global_setup)
  res$feedback
}

test_that("Basic exercise checking flow works", {
  # correct case
  sum_ex_correct <- get_exercise_result(
    user_code = "3 + 3",
    solution_code = "3 + 3",
    check_code = 'grade_result(
      pass_if_equals(x = 6, message = "You wrote the add!"),
      fail_if_equals(message = "Not quite the number we want."),
      user_result = last_value
    )'
  )
  testthat::expect_failure(testthat::expect_null(sum_ex_correct))
  testthat::expect_true(sum_ex_correct$correct)
  testthat::expect_equal(sum_ex_correct$type, "success")
  testthat::expect_match(sum_ex_correct$message, "You wrote the add!")

  # incorrect case
  sum_ex_incorrect <- get_exercise_result(
    user_code = "3 + 2",
    solution_code = "3 + 3",
    check_code = 'grade_result(
      pass_if_equals(x = 6, message = "You wrote the add!"),
      fail_if_equals(message = "Not quite the number we want."),
      user_result = last_value
    )'
  )
  testthat::expect_failure(testthat::expect_null(sum_ex_incorrect))
  testthat::expect_false(sum_ex_incorrect$correct)
  testthat::expect_equal(sum_ex_incorrect$type, "error")
  testthat::expect_match(sum_ex_incorrect$message, "Not quite the number we want.")
})

test_that("Exercise with basic setup works", {
  # correct case
  sum_setup_ex_correct <- get_exercise_result(
    user_code = "x + 3",
    solution_code = "x + 3",
    check_code = 'grade_result(
      pass_if_equals(x = 6, message = "You wrote the add!"),
      fail_if_equals(message = "Not quite the number we want."),
      user_result = last_value
    )',
    chunks = list(
      learnr:::mock_chunk("ex-setup", "x = 3", engine = "python")
    ),
    exercise.setup = "ex-setup"
  )
  testthat::expect_failure(testthat::expect_null(sum_setup_ex_correct))
  testthat::expect_true(sum_setup_ex_correct$correct)
  testthat::expect_equal(sum_setup_ex_correct$type, "success")
  testthat::expect_match(sum_setup_ex_correct$message, "You wrote the add!")

  # incorrect case
  sum_setup_ex_incorrect <- get_exercise_result(
    user_code = "x + 2",
    solution_code = "x + 3",
    check_code = 'grade_result(
      pass_if_equals(x = 6, message = "You wrote the add!"),
      fail_if_equals(message = "Not quite the number we want."),
      user_result = last_value
    )',
    chunks = list(
      learnr:::mock_chunk("ex-setup", "x = 3", engine = "python")
    ),
    exercise.setup = "ex-setup"
  )
  testthat::expect_failure(testthat::expect_null(sum_setup_ex_incorrect))
  testthat::expect_false(sum_setup_ex_incorrect$correct)
  testthat::expect_equal(sum_setup_ex_incorrect$type, "error")
  testthat::expect_match(sum_setup_ex_incorrect$message, "Not quite the number we want.")
})

test_that("Exercise with chained setup chunks works", {
  # correct case
  sum_chained_setup_ex_correct <- get_exercise_result(
    user_code = "y + 3",
    solution_code = "y + 3",
    check_code = 'grade_result(
      pass_if_equals(x = 9, message = "You wrote the add!"),
      fail_if_equals(message = "Not quite the number we want."),
      user_result = last_value
    )',
    chunks = list(
      learnr:::mock_chunk("first-setup", "x = 3", engine = "python"),
      learnr:::mock_chunk("second-setup", "y = x + 3", engine = "python", exercise.setup = "first-setup")
    ),
    setup_label = "second-setup"
  )
  testthat::expect_failure(testthat::expect_null(sum_chained_setup_ex_correct))
  testthat::expect_true(sum_chained_setup_ex_correct$correct)
  testthat::expect_equal(sum_chained_setup_ex_correct$type, "success")
  testthat::expect_match(sum_chained_setup_ex_correct$message, "You wrote the add!")

  # incorrect case
  sum_chained_setup_ex_incorrect <- get_exercise_result(
    user_code = "y + 1",
    solution_code = "y + 3",
    check_code = 'grade_result(
      pass_if_equals(x = 9, message = "You wrote the add!"),
      fail_if_equals(message = "Not quite the number we want."),
      user_result = last_value
    )',
    chunks = list(
      learnr:::mock_chunk("first-setup", "x = 3", engine = "python"),
      learnr:::mock_chunk("second-setup", "y = x + 3", engine = "python", exercise.setup = "first-setup")
    ),
    setup_label = "second-setup"
  )
  testthat::expect_failure(testthat::expect_null(sum_chained_setup_ex_incorrect))
  testthat::expect_false(sum_chained_setup_ex_incorrect$correct)
  testthat::expect_equal(sum_chained_setup_ex_incorrect$type, "error")
  testthat::expect_match(sum_chained_setup_ex_incorrect$message, "Not quite the number we want.")
})

test_that("Exercise with a global setup chunk works", {
  # only variables
  global_simple_ex_correct <- get_exercise_result(
    user_code = "z",
    solution_code = "z",
    check_code = 'grade_result(
      pass_if_equals(x = 3, message = "You got the number!"),
      fail_if_equals(message = "Not quite the number we want."),
      user_result = last_value
    )',
    global_setup = 'reticulate::py_run_string("x = 1; y = x + 1; z = y + 1", convert=FALSE)',
    evaluate_global_setup = TRUE
  )
  testthat::expect_failure(testthat::expect_null(global_simple_ex_correct))
  testthat::expect_true(global_simple_ex_correct$correct)
  testthat::expect_equal(global_simple_ex_correct$type, "success")
  testthat::expect_match(global_simple_ex_correct$message, "You got the number!")

  global_simple_ex_incorrect <- get_exercise_result(
    user_code = "z + 1",
    solution_code = "z",
    check_code = 'grade_result(
      pass_if_equals(x = 3, message = "You got the number!"),
      fail_if_equals(message = "Not quite the number we want."),
      user_result = last_value
    )',
    global_setup = 'reticulate::py_run_string("x = 1; y = x + 1; z = y + 1", convert=FALSE)',
    evaluate_global_setup = TRUE
  )
  testthat::expect_failure(testthat::expect_null(global_simple_ex_incorrect))
  testthat::expect_false(global_simple_ex_incorrect$correct)
  testthat::expect_equal(global_simple_ex_incorrect$type, "error")
  testthat::expect_match(global_simple_ex_incorrect$message, "Not quite the number we want.")

  # setup of imports
  global_imports_ex_correct <- get_exercise_result(
    user_code = 'pd.DataFrame({"a": [1, 2, 3]})',
    solution_code = 'pd.DataFrame({"a": [1, 2, 3]})',
    check_code = 'grade_result(
      pass_if_equals(x = pd.DataFrame({"a": [1, 2, 3]}), message = "You got the dataframe!"),
      fail_if_equals(message = "Not quite."),
      user_result = last_value
    )',
    global_setup = 'reticulate::py_run_string("import pandas as pd", convert=FALSE)',
    evaluate_global_setup = TRUE
  )
  testthat::expect_failure(testthat::expect_null(global_imports_ex_correct))
  testthat::expect_true(global_imports_ex_correct$correct)
  testthat::expect_equal(global_imports_ex_correct$type, "success")
  testthat::expect_match(global_imports_ex_correct$message, "You got the dataframe!")

  global_imports_ex_incorrect <- get_exercise_result(
    user_code = 'pd.DataFrame({"a": [1, 1, 3]})',
    solution_code = 'pd.DataFrame({"a": [1, 2, 3]})',
    check_code = 'grade_result(
      pass_if_equals(x = pd.DataFrame({"a": [1, 2, 3]}), message = "You got the dataframe!"),
      fail_if_equals(message = "Not quite."),
      user_result = last_value
    )',
    global_setup = 'reticulate::py_run_string("import pandas as pd", convert=FALSE)',
    evaluate_global_setup = TRUE
  )
  testthat::expect_failure(testthat::expect_null(global_imports_ex_incorrect))
  testthat::expect_false(global_imports_ex_incorrect$correct)
  testthat::expect_equal(global_imports_ex_incorrect$type, "error")
  testthat::expect_match(global_imports_ex_incorrect$message, "Not quite.")
})