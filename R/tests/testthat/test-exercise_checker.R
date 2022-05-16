reticulate::use_virtualenv("~/.venvs/pygradethis")
library(learnr)
library(pygradethis)
library(reticulate)

# helper function to test the exercise checker
get_exercise_result <- function(user_code, solution_code, last_value, check_code, setup_code = "") {
  envir_prep <- new.env()
  reticulate::py_run_string(setup_code)
  # copy the `py` into `envir_prep`
  envir_prep <- learnr::duplicate_py_env(py)
  # then save the new `py` into envir_result
  reticulate::py_run_string(user_code)
  envir_result <- learnr::duplicate_py_env(py)
  # envir_prep and envir_result should be different
  expect_false(identical(names(envir_prep), envir_result))
  pygradethis::exercise_checker(
    label = "ex-sum",
    solution_code = solution_code,
    user_code = user_code,
    check_code = check_code,
    envir_prep = envir_prep,
    envir_result = envir_result,
    last_value = last_value
  )
}

test_that("Exercise checker works", {
  # correct case
  sum_ex_correct <- get_exercise_result(
    user_code = "3 + 3", 
    solution_code = "3 + 3",
    last_value = 6,
    check_code = 'grade_result(
      pass_if_equals(x = 6, message = "You wrote the add!"),
      fail_if_equals(message = "Not quite the number we want."),
      user_result = last_value
    )'
  )
  testthat::expect_match(sum_ex_correct$message, "You wrote the add!")
  testthat::expect_true(sum_ex_correct$correct)
  testthat::expect_equal(sum_ex_correct$type, "success")

  # incorrect case
  sum_ex_incorrect <- get_exercise_result(
    user_code = "3 + 2", 
    solution_code = "3 + 3",
    last_value = 5,
    check_code = 'grade_result(
      pass_if_equals(x = 6, message = "You wrote the add!"),
      fail_if_equals(message = "Not quite the number we want."),
      user_result = last_value
    )'
  )
  # TODO there is a bug where the message of the fail if is not being used
  testthat::expect_match(sum_ex_incorrect$message, "Not quite the number we want.")
  testthat::expect_false(sum_ex_incorrect$correct)
  testthat::expect_equal(sum_ex_incorrect$type, "error")

  # exercise with setup code
  # correct case
  sum_setup_ex_correct <- get_exercise_result(
    setup_code = "x = 3",
    user_code = "x + 3",
    solution_code = "x + 3",
    last_value = 6,
    check_code = 'grade_result(
      pass_if_equals(x = 6, message = "You wrote the add!"),
      fail_if_equals(message = "Not quite the number we want."),
      user_result = last_value
    )'
  )
  testthat::expect_match(sum_setup_ex_correct$message, "You wrote the add!")
  testthat::expect_true(sum_setup_ex_correct$correct)
  testthat::expect_equal(sum_setup_ex_correct$type, "success")

  # incorrect case
  # correct case
  sum_setup_ex_incorrect <- get_exercise_result(
    setup_code = "x = 3",
    user_code = "x + 2",
    solution_code = "x + 3",
    last_value = 5,
    check_code = 'grade_result(
      pass_if_equals(x = 6, message = "You wrote the add!"),
      fail_if_equals(message = "Not quite the number we want."),
      user_result = last_value
    )'
  )
  testthat::expect_match(sum_setup_ex_incorrect$message, "Not quite the number we want.")
  testthat::expect_false(sum_setup_ex_incorrect$correct)
  testthat::expect_equal(sum_setup_ex_incorrect$type, "error")
})
