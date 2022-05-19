library(reticulate)

# helper function to test the exercise checker through the learnr flow
get_exercise_result <- function(label = "ex", setup_code = "", setup_label = "", user_code, solution_code, check_code) {
  args <- list(
    label = label,
    user_code = user_code,
    solution_code = solution_code,
    engine = "python",
    check = check_code,
    exercise.checker = learnr:::dput_to_string(pygradethis::exercise_checker)
  )
  # for creating a setup chunk
  if (nzchar(setup_code) && nzchar(setup_label)) {
    args <- append(args,
      list(
        chunks = list(
          learnr:::mock_chunk(setup_label, setup_code, engine = "python")
        ),
        exercise.setup = setup_label
      )
    )
  }
  ex <- do.call(learnr:::mock_exercise, args)
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
  testthat::expect_match(sum_ex_correct$message, "You wrote the add!")
  testthat::expect_true(sum_ex_correct$correct)
  testthat::expect_equal(sum_ex_correct$type, "success")

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
  testthat::expect_match(sum_ex_incorrect$message, "Not quite the number we want.")
  testthat::expect_false(sum_ex_incorrect$correct)
  testthat::expect_equal(sum_ex_incorrect$type, "error")

  ### Exercise with setup code

  # correct case
  sum_setup_ex_correct <- get_exercise_result(
    setup_label = "ex-setup",
    setup_code = "x = 3",
    user_code = "x + 3",
    solution_code = "x + 3",
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
  sum_setup_ex_incorrect <- get_exercise_result(
    setup_label = "ex-setup",
    setup_code = "x = 3",
    user_code = "x + 2",
    solution_code = "x + 3",
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
