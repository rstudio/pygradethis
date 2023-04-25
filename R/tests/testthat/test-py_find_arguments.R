test_that("py_find_arguments() without match works", {
  # no arg
  found <- with_py_clear_env({
    .user_code <- "sum()"
    py_find_arguments()
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 0)

  # 1 arg
  found <- with_py_clear_env({
    .user_code <- "sum([1, 2.5, 3])"
    py_find_arguments()
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 1)

  # multiple args
  found <- with_py_clear_env({
    .user_code <- "sum([1, 2.5, 3])\nround(2.5)"
    py_find_arguments()
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 2)

  # nested args
  found <- with_py_clear_env({
    .user_code <- "sum([1, round(2.5), 3])"
    py_find_arguments()
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 2)

  # mix of positional and keywords
  found <- with_py_clear_env({
    .user_code <- 'print("Hello", "World!", 2.5, sep=", ")'
    py_find_arguments()
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 4)
})

test_that("py_find_arguments() with match works", {
  # 1 arg
  found <- with_py_clear_env({
    .user_code <- "sum([1, 2.5, 3])"
    py_find_arguments(match = py_args("[1, 2.5, 3]"))
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 1)

  # multiple args
  found <- with_py_clear_env({
    .user_code <- "sum([1, 2.5, 3])\nround(2.5)"
    py_find_arguments(match = py_args("[1, 2.5, 3]", "2.5"))
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 2)

  # 1 keyword arg
  found <- with_py_clear_env({
    .user_code <- 'print("Hello", "World!", 2.5, sep=", ", end="\\n")'
    py_find_arguments(match = py_args(sep = '", "'))
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 1)

  # multiple keywords
  found <- with_py_clear_env({
    .user_code <- 'print("Hello", "World!", 2.5, sep=", ", end="\\n")'
    py_find_arguments(match = py_args(sep = '", "', end = '"\\n"'))
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 2)

  # mix of positional / keywords args and literals versus code text
  found <- with_py_clear_env({
    .user_code <- 'print("Hello", "World!", 2.5, sep=", ", end="\\n")'
    py_find_arguments(match = py_args(
      '"Hello"', '"World!"', "2.5",
      sep = '", "', end = '"\\n"'
    ))
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 5)

  # py_literal() also works as alternative to double quoting strings for py_args()
  found <- with_py_clear_env({
    .user_code <- 'print("Hello", "World!", 2.5, sep=", ", end="\\n")'
    py_find_arguments(match = py_args(
      py_literal("Hello"), py_literal("World!"), "2.5",
      sep = '", "', end = '"\\n"'
    ))
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 5)
})
