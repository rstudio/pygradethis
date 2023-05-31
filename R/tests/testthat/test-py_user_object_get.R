# User objects ----

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
  expect_false(py_user_object_exists("invalid"))
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
  expect_null(py_user_object_get("invalid"))
})

# Solution objects ----

test_that("py_solution_object_list() works", {
  # no new objects
  setup <- "x = 2"
  solution_code <- "x = 2"
  .py_envir_prep <- reticulate::py_run_string(setup, local = TRUE, convert = FALSE)
  .py_envir_solution <- reticulate::py_run_string(
    paste0(c(setup, solution_code), collapse = "\n"),
    local = TRUE,
    convert = FALSE
  )
  expect_equal(py_solution_object_list(), list())

  # new objects
  setup <- "x = 2\nsetup_var = 2"
  solution_code <- "y = x + 1\nz = y + 1"
  .py_envir_prep <- reticulate::py_run_string(setup, local = TRUE, convert = FALSE)
  .py_envir_solution <- reticulate::py_run_string(
    paste0(c(setup, solution_code), collapse = "\n"),
    local = TRUE,
    convert = FALSE
  )
  sol_objs <- py_solution_object_list()
  expect_equal(sol_objs, c("y", "z"))
  expect_true(all(!c("x", "setup_var") %in% sol_objs))
})

test_that("py_solution_object_exists() works", {
  # no new objects
  setup <- "x = 2"
  user_code <- "y = x + 1"
  solution_code <- "y = x + 1\nz = y + 1"
  .py_envir_prep <- reticulate::py_run_string(setup, local = TRUE, convert = FALSE)
  .py_envir_solution <- reticulate::py_run_string(
    paste0(c(setup, solution_code), collapse = "\n"),
    local = TRUE,
    convert = FALSE
  )
  expect_true(py_solution_object_exists("x"))
  expect_true(py_solution_object_exists("y"))
  expect_true(py_solution_object_exists("z"))
  expect_false(py_solution_object_exists("invalid"))
})

test_that("py_solution_object_get() works", {
  # no new objects
  setup <- "x = 2"
  user_code <- "y = x + 1\nz = y + 1"
  solution_code <- "y = x + 1\nz = y + 1"
  .py_envir_prep <- reticulate::py_run_string(setup, local = TRUE, convert = FALSE)
  .py_envir_solution <- reticulate::py_run_string(
    paste0(c(setup, user_code), collapse = "\n"),
    local = TRUE,
    convert = FALSE
  )
  expect_identical(py_solution_object_get("x"), reticulate::py_eval("2", convert = FALSE))
  expect_identical(py_solution_object_get("y"), reticulate::py_eval("3", convert = FALSE))
  expect_identical(py_solution_object_get("z"), reticulate::py_eval("4", convert = FALSE))
  expect_null(py_solution_object_get("invalid"))
})
