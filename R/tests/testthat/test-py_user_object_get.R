
test_that("py_user_object_list() works", {
  # NOTE: mocking relevant gradethis objects is the simplest way to mock this for Python
  # currently we can't fully mock a Python exercise AND be able to check the functions behavior

  # no new objects
  setup <- "x = 2"
  user_code <- "x = 2"
  .py_envir_prep <- reticulate::py_run_string(setup, local = TRUE, convert = FALSE)
  .py_envir_result <- reticulate::py_run_string(
    paste0(c(setup, user_code), collapse = "\n"),
    local = TRUE,
    convert = FALSE
  )
  expect_equal(py_user_object_list(), list())

  # some new objects
  setup <- "x = 2"
  user_code <- "y = x + 1\nz = y + 1"
  .py_envir_prep <- reticulate::py_run_string(setup, local = TRUE, convert = FALSE)
  .py_envir_result <- reticulate::py_run_string(
    paste0(c(setup, user_code), collapse = "\n"),
    local = TRUE,
    convert = FALSE
  )
  expect_equal(py_user_object_list(), c("y", "z"))
})

# TODO implement/test the solution object list

test_that("py_user_object_exists() works", {
  # no new objects
  setup <- "x = 2"
  user_code <- "y = x + 1\nz = y + 1"
  .py_envir_prep <- reticulate::py_run_string(setup, local = TRUE, convert = FALSE)
  .py_envir_result <- reticulate::py_run_string(
    paste0(c(setup, user_code), collapse = "\n"),
    local = TRUE,
    convert = FALSE
  )
  .py_envir_solution <- reticulate::py_run_string(
    paste0(c(setup, user_code), collapse = "\n"),
    local = TRUE,
    convert = FALSE
  )
  expect_true(py_user_object_exists("x"))
  expect_true(py_user_object_exists("y"))
  expect_true(py_user_object_exists("z"))
})

test_that("py_user_object_get() works", {
  # no new objects
  setup <- "x = 2"
  user_code <- "y = x + 1\nz = y + 1"
  .py_envir_prep <- reticulate::py_run_string(setup, local = TRUE, convert = FALSE)
  .py_envir_result <- reticulate::py_run_string(
    paste0(c(setup, user_code), collapse = "\n"),
    local = TRUE,
    convert = FALSE
  )
  .py_envir_solution <- reticulate::py_run_string(
    paste0(c(setup, user_code), collapse = "\n"),
    local = TRUE,
    convert = FALSE
  )
  expect_identical(py_user_object_get("x"), reticulate::py_eval("2", convert = FALSE))
  expect_identical(py_user_object_get("y"), reticulate::py_eval("3", convert = FALSE))
  expect_identical(py_user_object_get("z"), reticulate::py_eval("4", convert = FALSE))
})

test_that("py_solution_object_exists() works", {
  # no new objects
  setup <- "x = 2"
  user_code <- "y = x + 1"
  solution_code <- "y = x + 1\nz = y + 1"
  .py_envir_prep <- reticulate::py_run_string(setup, local = TRUE, convert = FALSE)
  .py_envir_result <- reticulate::py_run_string(
    paste0(c(setup, user_code), collapse = "\n"),
    local = TRUE,
    convert = FALSE
  )
  .py_envir_solution <- reticulate::py_run_string(
    paste0(c(setup, solution_code), collapse = "\n"),
    local = TRUE,
    convert = FALSE
  )
  expect_true(py_solution_object_exists("x"))
  expect_true(py_solution_object_exists("y"))
  expect_true(py_solution_object_exists("z"))
})

test_that("py_solution_object_get() works", {
  # no new objects
  setup <- "x = 2"
  user_code <- "y = x + 1\nz = y + 1"
  solution_code <- "y = x + 1\nz = y + 1"
  .py_envir_prep <- reticulate::py_run_string(setup, local = TRUE, convert = FALSE)
  .py_envir_result <- reticulate::py_run_string(
    paste0(c(setup, user_code), collapse = "\n"),
    local = TRUE,
    convert = FALSE
  )
  .py_envir_solution <- reticulate::py_run_string(
    paste0(c(setup, user_code), collapse = "\n"),
    local = TRUE,
    convert = FALSE
  )
  expect_identical(py_solution_object_get("x"), reticulate::py_eval("2", convert = FALSE))
  expect_identical(py_solution_object_get("y"), reticulate::py_eval("3", convert = FALSE))
  expect_identical(py_solution_object_get("z"), reticulate::py_eval("4", convert = FALSE))
})