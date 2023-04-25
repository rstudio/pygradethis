test_that("py_find_functions() without match works", {
  # no calls
  found <- with_py_clear_env({
    .user_code <- "[1, 2.5, 3]"
    py_find_functions()
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 0)

  # multiple calls
  found <- with_py_clear_env({
    .user_code <- "sum([1, 2, 3])\nround(2.5)"
    py_find_functions()
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 2)

  # nested calls
  found <- with_py_clear_env({
    .user_code <- "sum([1, round(2.5), 3])"
    py_find_functions()
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 2)

  # method call
  found <- with_py_clear_env({
    .user_code <- "df.info()"
    py_find_functions()
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 1)

  # multiple method call
  found <- with_py_clear_env({
    .user_code <- "df.info()\ndf.head()"
    py_find_functions()
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 2)
})

test_that("py_find_functions() with match works", {
  # find sum()
  found <- with_py_clear_env({
    .user_code <- "sum([1, 2, 3])\nround(2.5)"
    py_find_functions(match = "sum")
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 1)
  
  # find round()
  found <- with_py_clear_env({
    .user_code <- "sum([1, 2, 3])\nround(2.5)"
    py_find_functions(match = "round")
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 1)

  # find .info()
  found <- with_py_clear_env({
    .user_code <- "df.info()\ndf.head()"
    py_find_functions(match = "info")
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 1)

  # find .head()
  found <- with_py_clear_env({
    .user_code <- "df.info()\ndf.head()"
    py_find_functions(match = "head")
  })
  testthat::expect_identical(pygradethis::get_friendly_class(found), "GradeCodeFound")
  testthat::expect_true(length(found$last_result) == 1)
})
