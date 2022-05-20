library(reticulate)

# helper function to test the exercise checker through the learnr flow
get_exercise_result <- function(label = "ex", user_code, solution_code, check_code, ...) {
  ex <- learnr:::mock_exercise(
    label = label,
    user_code = user_code,
    solution_code = solution_code,
    engine = "python",
    check = check_code,
    exercise.checker = learnr:::dput_to_string(pygradethis::exercise_checker),
    ...
  )
  res <- learnr:::evaluate_exercise(ex, envir = new.env())
  res$feedback
}

test_that("Exercise checking flow works", {
  ### Simple exercise with no setup code

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

  ### Exercise with setup code

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

  ### Exercise with chained setup code

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
