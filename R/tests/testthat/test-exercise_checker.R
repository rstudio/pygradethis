reticulate::use_virtualenv("~/.venvs/pygradethis")
library(learnr)
library(pygradethis)
library(reticulate)

test_that("Exercise checker works", {
  # correct case
  # first store the envir_prep that's a duplicate of global
  envir_prep <- new.env()
  # copy the `py` into `envir_prep`
  envir_prep <- duplicate_py_env(py) # the `py` module can be accessed in Python side!
  # then save the new `py` into envir_result
  reticulate::py_run_string("3 + 3")
  envir_result <- duplicate_py_env(py)
  # envir_prep and envir_result should be different
  expect_false(identical(names(envir_prep), envir_result))
  # run exercise code
  result <- exercise_checker(
      label = "ex-sum",
      solution_code = "6",
      user_code = "3 + 3",
      check_code = 'python_grade_result(
      python_pass_if(6, "You wrote the add!"),
      python_fail_if(True, "Not quite the number we want."),
      user_result = last_value
    )',
    envir_prep = envir_prep,
    envir_result = envir_result,
    last_value = 6
  )
  testthat::expect_match(result$message, "You wrote the add!")
  testthat::expect_true(result$correct)
  testthat::expect_equal(result$type, "success")

  # incorrect case
  # first store the envir_prep that's a duplicate of global
  learnr:::clear_py_env()
  envir_prep <- new.env()
  envir_prep <- duplicate_py_env(py) # the `py` module can be accessed in Python side!
  reticulate::py_run_string("3 + 2")
  envir_result <- duplicate_py_env(py)
  expect_false(identical(names(envir_prep), envir_result))
  result <- exercise_checker(
      label = "ex-sum",
      solution_code = "6",
      user_code = "3 + 2",
      check_code = 'python_grade_result(
      python_pass_if(6, "You wrote the add!"),
      python_fail_if(5, "Not quite the number we want."),
      user_result = last_value
    )',
    envir_prep = envir_prep,
    envir_result = envir_result,
    last_value = 5
  )
  testthat::expect_match(result$message, "Not quite the number we want.")
  testthat::expect_false(result$correct)
  testthat::expect_equal(result$type, "error")

  # exercise with setup code
  # correct case
  # first store the envir_prep that's a duplicate of global
  learnr:::clear_py_env()
  envir_prep <- new.env()
  reticulate::py_run_string("x = 3")
  envir_prep <- duplicate_py_env(py) 
  reticulate::py_run_string("x + 3")
  envir_result <- duplicate_py_env(py)
  expect_false(identical(names(envir_prep), envir_result))
  # run exercise code
  result <- exercise_checker(
      label = "ex-sum",
      solution_code = "6",
      user_code = "x + 3",
      check_code = 'python_grade_result(
      python_pass_if(6, "You wrote the add!"),
      python_fail_if(True, "Not quite the number we want."),
      user_result = last_value
    )',
    envir_prep = envir_prep,
    envir_result = envir_result,
    last_value = 6
  )
  testthat::expect_match(result$message, "You wrote the add!")
  testthat::expect_true(result$correct)
  testthat::expect_equal(result$type, "success")

  # incorrect case
  # first store the envir_prep that's a duplicate of global
  learnr:::clear_py_env()
  envir_prep <- new.env()
  reticulate::py_run_string("x = 3")
  envir_prep <- duplicate_py_env(py) 
  reticulate::py_run_string("x + 2")
  envir_result <- duplicate_py_env(py)
  expect_false(identical(names(envir_prep), envir_result))
  # run exercise code
  result <- exercise_checker(
      label = "ex-sum",
      solution_code = "6",
      user_code = "x + 2",
      check_code = 'python_grade_result(
      python_pass_if(6, "You wrote the add!"),
      python_fail_if(5, "Not quite the number we want."),
      user_result = last_value
    )',
    envir_prep = envir_prep,
    envir_result = envir_result,
    last_value = 5
  )
  testthat::expect_match(result$message, "Not quite the number we want.")
  testthat::expect_false(result$correct)
  testthat::expect_equal(result$type, "error")
})
