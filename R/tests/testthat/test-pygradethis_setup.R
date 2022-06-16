
test_that("Exercise with a global setup chunk works", {
  # only variables
  global_ex_correct <- mock_py_exercise(
    user_code = "z",
    solution_code = "z",
    check = 'grade_result(
      pass_if_equals(x = 3, message = "You got the number!"),
      fail_if_equals(message = "Not quite the number we want."),
      user_result = last_value
    )',
    global_setup = 'add_global_setup("x = 1; y = x + 1; z = y + 1")'
  )
  feedback <- evaluate_exercise_feedback(global_ex_correct, evaluate_global_setup = TRUE)
  expect_failure(expect_null(feedback))
  expect_true(feedback$correct)
  expect_equal(feedback$type, "success")
  expect_match(feedback$message, "You got the number!")

  ex_incorrect <- mock_py_exercise(
    user_code = "z + 1",
    solution_code = "z",
    check = 'grade_result(
      pass_if_equals(x = 3, message = "You got the number!"),
      fail_if_equals(message = "Not quite the number we want."),
      user_result = last_value
    )',
    global_setup = 'add_global_setup("x = 1; y = x + 1; z = y + 1")'
  )
  feedback <- evaluate_exercise_feedback(ex_incorrect, evaluate_global_setup = TRUE)
  expect_failure(expect_null(feedback))
  expect_false(feedback$correct)
  expect_equal(feedback$type, "error")
  expect_match(feedback$message, "Not quite the number we want.")
})

test_that("Exercise with global imports works", {
  # setup of imports
  ex_correct <- mock_py_exercise(
    user_code = 'pd.DataFrame({"a": [1, 2, 3]})',
    solution_code = 'pd.DataFrame({"a": [1, 2, 3]})',
    check = 'grade_result(
      pass_if_equals(x = pd.DataFrame({"a": [1, 2, 3]}), message = "You got the dataframe!"),
      fail_if_equals(message = "Not quite."),
      user_result = last_value
    )',
    global_setup = 'add_global_setup("import pandas as pd")'
  )
  feedback <- evaluate_exercise_feedback(ex_correct, evaluate_global_setup = TRUE)
  expect_failure(expect_null(feedback))
  expect_true(feedback$correct)
  expect_equal(feedback$type, "success")
  expect_match(feedback$message, "You got the dataframe!")

  ex_incorrect <- mock_py_exercise(
    user_code = 'pd.DataFrame({"a": [1, 2]})',
    solution_code = 'pd.DataFrame({"a": [1, 2, 3]})',
    check = 'grade_result(
      pass_if_equals(x = pd.DataFrame({"a": [1, 2, 3]}), message = "You got the dataframe!"),
      fail_if_equals(message = "Not quite."),
      user_result = last_value
    )',
    global_setup = 'add_global_setup("import pandas as pd")'
  )
  feedback <- evaluate_exercise_feedback(ex_incorrect, evaluate_global_setup = TRUE)
  expect_failure(expect_null(feedback))
  expect_false(feedback$correct)
  expect_equal(feedback$type, "error")
  expect_match(feedback$message, "Not quite.")
})
