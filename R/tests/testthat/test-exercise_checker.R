#### Basic flow tests

test_that("Basic exercise checking flow works", {
  ex <- mock_py_exercise(
    user_code = "3 + 3",
    solution_code = "3 + 3",
    check = 'Graded(x = last_value)'
  )
  feedback <- evaluate_exercise_feedback(ex)
  expect_failure(expect_null(feedback))
  expect_s3_class(feedback, c("list", "gradethis_graded"))

  # incorrect case
  ex <- mock_py_exercise(
    user_code = "3 + 2",
    solution_code = "3 + 3",
    check = 'Graded(x = 5)'
  )
  feedback <- evaluate_exercise_feedback(ex)
  expect_failure(expect_null(feedback))
  expect_s3_class(feedback, c("list", "gradethis_graded"))
})

# TODO add tests for the `py_gradethis_exercise_checker`
