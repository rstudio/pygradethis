test_that("py_to_r() translates DataFrames", {
  # NOTE: to be safe, we isolate reticulate calls to a fresh R process
  py_tbl_df <- with_py_clear_env({
    library(reticulate)
    # setup Python libraries
    reticulate::py_run_string('import pandas as pd; import numpy as np')
    pygradethis::py_to_r(reticulate::py_eval(
      'pd.DataFrame({"a":[1,2,3]})',
      convert = FALSE
    ))
  })
  expected_tbl <- tibble::tibble(a = c(1, 2, 3))
  class(expected_tbl) <- c("py_tbl_df", class(expected_tbl))
  testthat::expect_equal(py_tbl_df, expected_tbl)
})

test_that("py_to_r() translates Series", {
  py_series <- with_py_clear_env({
    library(reticulate)
    reticulate::py_run_string('import pandas as pd; import numpy as np')
    pygradethis::py_to_r(reticulate::py_eval(
      'pd.Series([1,2,3])',
      convert = FALSE
    ))
  })
  expected_series <- as.array(c("0" = 1, "1" = 2, "2" = 3))
  testthat::expect_equal(py_series, expected_series)
})

test_that("py_to_r() translates DataFrames w/ a MultiIndex", {
  py_multi_index <- with_py_clear_env({
    library(reticulate)
    reticulate::py_run_string('import pandas as pd; import numpy as np')
    py_multi_df <- reticulate::py_run_string(
      'multi_index =  pd.MultiIndex.from_tuples([("A", 1), ("A", 2),("A", 3), ("B", 1),("B", 2)])\ndf = pd.DataFrame({"a":[2,3,4,5,6],"b":[7,8,9,10,11]}, index=multi_index)',
      convert = FALSE
    )$df
    pygradethis::py_to_r(py_multi_df)
  })
  expected_tbl <- tibble::tribble(
    ~a, ~b,
    2, 7,
    3, 8,
    4, 9,
    5, 10,
    6, 11
  )
  class(expected_tbl) <- c("py_tbl_df", class(expected_tbl))
  testthat::expect_equal(py_multi_index, expected_tbl)
})

test_that("py_to_tbl() translates DataFrame to tibble without groups", {
  py_tbl_df <- with_py_clear_env({
    library(reticulate)
    reticulate::py_run_string('import pandas as pd; import numpy as np')
    pygradethis::py_to_tbl(reticulate::py_eval(
      'pd.DataFrame({"Animal": ["Falcon","Falcon","Parrot","Parrot"], "Max Speed": [380., 370., 24., 26.]})', 
      convert = FALSE
    ))
  })
  expected_tbl <- tibble::tribble(
      ~Animal, ~`Max Speed`,
      "Falcon",   380,
      "Falcon",   370,
      "Parrot",   24,
      "Parrot",   26
  )
  class(expected_tbl) <- c("py_tbl_df", class(expected_tbl))
  testthat::expect_equal(py_tbl_df, expected_tbl)
})

testthat::test_that("py_to_tbl() translates DataFrame to tibble with single group", {
  py_tbl_df <- with_py_clear_env({
    library(reticulate)
    reticulate::py_run_string('import pandas as pd; import numpy as np')
    py_df <- reticulate::py_eval(
      'pd.DataFrame({"Animal": ["Falcon", "Falcon", "Parrot", "Parrot"], "Max Speed": [380., 370., 24., 26.]}).groupby(["Animal"]).mean()', 
      convert = FALSE
    )
    pygradethis::py_to_tbl(py_df)
  })
  expected_tbl <- tibble::tribble(
      ~Animal, ~`Max Speed`,
      "Falcon",   375,
      "Parrot",   25
  ) %>% dplyr::group_by(Animal)
  class(expected_tbl) <- c("py_grouped_df", "py_tbl_df", class(expected_tbl))
  testthat::expect_equal(py_tbl_df, expected_tbl)
})

testthat::test_that("py_to_tbl() translates DataFrame to tibble with multiple groups", {
  py_tbl_df <- with_py_clear_env({
    library(reticulate)
    reticulate::py_run_string('import pandas as pd; import numpy as np')
    py_df <- reticulate::py_eval('(
        pd.DataFrame(
        [
            ("bird", "Falconiformes", 389.0),
            ("bird", "Psittaciformes", 24.0),
            ("mammal", "Carnivora", 80.2),
            ("mammal", "Primates", np.nan),
            ("mammal", "Carnivora", 58),
        ],
        columns=("class", "order", "max_speed"),
      )
    ).groupby(["class", "order"]).mean()',
      convert = FALSE
    )
    pygradethis::py_to_tbl(py_df)
  })
  expected_tbl <- tibble::tribble(
      ~class, ~order, ~max_speed,
      "bird", "Falconiformes", 389.0,
      "bird", "Psittaciformes", 24.0,
      "mammal", "Carnivora", 69.1,
      "mammal", "Primates", NaN
  ) %>% dplyr::group_by(class, order)
  class(expected_tbl) <- c('py_grouped_df', 'py_tbl_df', class(expected_tbl))
  testthat::expect_equal(py_tbl_df, expected_tbl)
})

testthat::test_that("identical() works for Python types", {
  an_int <- pygradethis::py_to_r(reticulate::py_eval("1", convert=F))
  testthat::expect_true(identical(an_int, 1L))

  a_complex <- pygradethis::py_to_r(reticulate::py_eval("1 + 1j", convert=F))
  testthat::expect_true(identical(a_complex, complex(real=1, imaginary=1)))

  a_float <- pygradethis::py_to_r(reticulate::py_eval("1.0", convert=F))
  testthat::expect_true(identical(a_float, 1.0))

  a_bool <- pygradethis::py_to_r(reticulate::py_eval("True", convert=F))
  testthat::expect_true(identical(a_bool, TRUE))

  a_str <- pygradethis::py_to_r(reticulate::py_eval("'hello world'", convert=F))
  testthat::expect_true(identical(a_str, "hello world"))

  a_list <- pygradethis::py_to_r(reticulate::py_eval("[1, 2]", F))
  testthat::expect_true(identical(a_list, c(1L, 2L)))

  # Note: sometimes we have to unclass for e.g. the tuple type
  a_tuple <- pygradethis::py_to_r(reticulate::py_eval("(1,1)", convert=F))
  testthat::expect_true(identical(a_tuple, list(1L, 1L)))

  a_dict <- pygradethis::py_to_r(reticulate::py_eval("{'a': 1, 'b': 'foo'}", F))
  testthat::expect_true(identical(a_dict, list(a = 1L, b = "foo")))

  a_set <- pygradethis::py_to_r(reticulate::py_eval("{1, 2}", F))
  testthat::expect_true(identical(a_set, c(1L, 2L)))

  # any other type that we don't have a corresponding identical() method
  # will go through the identical.default() which will unclass objects
  other_type <- pygradethis::py_to_r(reticulate::py_eval("1", F))
  class(other_type) <- c("foo", "pygradethis")
  testthat::expect_true(identical(other_type, 1L))
})

testthat::test_that("waldo::compare() works for Python types", {
  an_int <- pygradethis::py_to_r(reticulate::py_eval("1", convert=F))
  testthat::expect_length(waldo::compare(an_int, 1L), 0)

  a_complex <- pygradethis::py_to_r(reticulate::py_eval("1 + 1j", convert=F))
  testthat::expect_length(waldo::compare(a_complex, complex(real=1, imaginary=1)), 0)

  a_float <- pygradethis::py_to_r(reticulate::py_eval("1.0", convert=F))
  testthat::expect_length(waldo::compare(a_float, 1.0), 0)

  a_bool <- pygradethis::py_to_r(reticulate::py_eval("True", convert=F))
  testthat::expect_length(waldo::compare(a_bool, TRUE), 0)

  a_str <- pygradethis::py_to_r(reticulate::py_eval("'hello world'", convert=F))
  testthat::expect_length(waldo::compare(a_str, "hello world"), 0)

  a_list <- pygradethis::py_to_r(reticulate::py_eval("[1, 2]", F))
  testthat::expect_length(waldo::compare(a_list, c(1L, 2L)), 0)

  # Note: sometimes we have to unclass for e.g. the tuple type
  a_tuple <- pygradethis::py_to_r(reticulate::py_eval("(1,1)", convert=F))
  testthat::expect_length(waldo::compare(a_tuple, list(1L, 1L)), 0)

  a_dict <- pygradethis::py_to_r(reticulate::py_eval("{'a': 1, 'b': 'foo'}", F))
  testthat::expect_length(waldo::compare(a_dict, list(a = 1L, b = "foo")), 0)

  a_set <- pygradethis::py_to_r(reticulate::py_eval("{1, 2}", F))
  testthat::expect_length(waldo::compare(a_set, c(1L, 2L)), 0)

  other_type <- pygradethis::py_to_r(reticulate::py_eval("1", F))
  class(other_type) <- c("foo", "pygradethis")
  testthat::expect_length(waldo::compare(other_type, 1L), 1)
})

testthat::test_that("pass_if_equal() and fail_if_equal() works with Python types", {
  # pass_if_equal()
  ex_pass_if_equal_correct <- learnr::mock_exercise(
    user_code = "56 + 44",
    solution_code = "56 + 44",
    engine = "python",
    check = "gradethis::grade_this({\n  gradethis::pass_if_equal(message='yay!')\n  gradethis::fail('boo!')\n})",
    exercise.checker = "pygradethis::py_gradethis_exercise_checker"
  )
  res <- learnr:::evaluate_exercise(ex_pass_if_equal_correct, new.env())
  testthat::expect_match(res$feedback$message, "yay!")

  ex_pass_if_equal_incorrect <- learnr::mock_exercise(
    user_code = "56",
    solution_code = "56 + 44",
    engine = "python",
    check = "gradethis::grade_this({\n  gradethis::pass_if_equal(message='yay!')\n  gradethis::fail('boo!')\n})",
    exercise.checker = "pygradethis::py_gradethis_exercise_checker"
  )
  res <- learnr:::evaluate_exercise(ex_pass_if_equal_incorrect, new.env())
  testthat::expect_match(res$feedback$message, "boo!")

  # fail_if_equal()
  ex_fail_if_equal_incorrect <- learnr::mock_exercise(
    user_code = "56",
    solution_code = "56 + 44",
    engine = "python",
    check = "gradethis::grade_this({\n  gradethis::fail_if_equal(y = 56, message='boo!')\n  gradethis::pass('yay!')\n})",
    exercise.checker = "pygradethis::py_gradethis_exercise_checker"
  )
  res <- learnr:::evaluate_exercise(ex_fail_if_equal_incorrect, new.env())
  testthat::expect_match(res$feedback$message, "boo!")

  ex_fail_if_equal_correct <- learnr::mock_exercise(
    user_code = "56 + 44",
    solution_code = "56 + 44",
    engine = "python",
    check = "gradethis::grade_this({\n  gradethis::fail_if_equal(y = 56, message='boo!')\n  gradethis::pass('yay!')\n})",
    exercise.checker = "pygradethis::py_gradethis_exercise_checker"
  )
  res <- learnr:::evaluate_exercise(ex_fail_if_equal_correct, new.env())
  testthat::expect_match(res$feedback$message, "yay!")
})
