
test_that("py_check_index() works", {
  check_index_correct <- callr::r_safe(function() {
    library(reticulate)
    reticulate::py_run_string('import pandas as pd; import numpy as np')
    .result <- reticulate::py_eval(
      "pd.DataFrame({'a':[1,2,3]})",
      convert = FALSE
    )
    .solution <- reticulate::py_eval(
      "pd.DataFrame({'a':[1,2,3]})",
      convert = FALSE
    )
    pygradethis::py_check_index(.result, .solution)
  })
  testthat::expect_true(check_index_correct)

  check_index_incorrect <- callr::r_safe(function() {
    library(reticulate)
    reticulate::py_run_string('import pandas as pd; import numpy as np')
    .result <- reticulate::py_eval(
      "pd.DataFrame({'a':[1,2]})",
      convert = FALSE
    )
    .solution <- reticulate::py_eval(
      "pd.DataFrame({'a':[1,2,3]})",
      convert = FALSE
    )
    pygradethis::py_check_index(.result, .solution)
  })
  testthat::expect_false(check_index_incorrect)
})

test_that("py_check_columns() works", {
  check_columns_correct <- callr::r_safe(function() {
    library(reticulate)
    reticulate::py_run_string("import pandas as pd; import numpy as np")
    .result <- reticulate::py_eval(
      "pd.DataFrame({'a':[1,2,3]})",
      convert = FALSE
    )
    .solution <- reticulate::py_eval(
      "pd.DataFrame({'a':[1,2,3]})",
      convert = FALSE
    )
    pygradethis::py_check_columns(.result, .solution)
  })
  testthat::expect_true(check_columns_correct)

  check_columns_incorrect <- callr::r_safe(function() {
    library(reticulate)
    reticulate::py_run_string("import pandas as pd; import numpy as np")
    .result <- reticulate::py_eval(
      "pd.DataFrame({'a':[1,2,3]})",
      convert = FALSE
    )
    .solution <- reticulate::py_eval(
      "pd.DataFrame({'b':[1,2,3]})",
      convert = FALSE
    )
    pygradethis::py_check_columns(.result, .solution)
  })
  testthat::expect_false(check_columns_incorrect)
})

test_that("py_check_values() works", {
  # TODO we should check various different types of columns
  check_values_correct <- callr::r_safe(function() {
    library(reticulate)
    reticulate::py_run_string("import pandas as pd; import numpy as np")
    .result <- reticulate::py_eval(
      "pd.DataFrame({'a':[1,2,3], 'b':['a', 'b', 'c']})",
      convert = FALSE
    )
    .solution <- reticulate::py_eval(
      "pd.DataFrame({'a':[1,2,3], 'b':['a', 'b', 'c']})",
      convert = FALSE
    )
    pygradethis::py_check_values(.result, .solution)
  })
  testthat::expect_true(check_values_correct)

  check_values_incorrect <- callr::r_safe(function() {
    library(reticulate)
    reticulate::py_run_string("import pandas as pd; import numpy as np")
    .result <- reticulate::py_eval(
      "pd.DataFrame({'a':[1,2,99]})",
      convert = FALSE
    )
    .solution <- reticulate::py_eval(
      "pd.DataFrame({'b':[1,2,3]})",
      convert = FALSE
    )
    pygradethis::py_check_values(.result, .solution)
  })
  testthat::expect_false(check_values_incorrect)
})

test_that("py_check_dataframe() works", {
  check_dataframe_correct <- callr::r_safe(function() {
    library(reticulate)
    reticulate::py_run_string("import pandas as pd; import numpy as np")
    .result <- reticulate::py_eval(
      "pd.DataFrame({'a':[1,2,3]})",
      convert = FALSE
    )
    .solution <- reticulate::py_eval(
      "pd.DataFrame({'a':[1,2,3]})",
      convert = FALSE
    )
    pygradethis::py_check_dataframe(.result, .solution)
  })
  testthat::expect_null(check_dataframe_correct)

  check_dataframe_problem <- callr::r_safe(function() {
    library(reticulate)
    reticulate::py_run_string("import pandas as pd; import numpy as np")
    .result <- reticulate::py_eval(
      "pd.DataFrame({'a':[1,2,99]})",
      convert = FALSE
    )
    .solution <- reticulate::py_eval(
      "pd.DataFrame({'b':[1,2,3]})",
      convert = FALSE
    )
    pygradethis::py_check_dataframe(.result, .solution)
  })
  testthat::expect_true(tblcheck::is_tblcheck_problem(check_dataframe_problem))
  testthat::expect_false(tblcheck::tblcheck_grade(check_dataframe_problem)$correct)
})

test_that("py_check_series() works", {
  check_series_correct <- callr::r_safe(function() {
    library(reticulate)
    reticulate::py_run_string("import pandas as pd; import numpy as np")
    .result <- reticulate::py_eval(
      "pd.Series([1,2,3])",
      convert = FALSE
    )
    .solution <- reticulate::py_eval(
      "pd.Series([1,2,3])",
      convert = FALSE
    )
    pygradethis::py_check_series(.result, .solution)
  })
  testthat::expect_true(check_series_correct)

  check_series_incorrect <- callr::r_safe(function() {
    library(reticulate)
    reticulate::py_run_string("import pandas as pd; import numpy as np")
    .result <- reticulate::py_eval(
      "pd.Series([1,2,4])",
      convert = FALSE
    )
    .solution <- reticulate::py_eval(
      "pd.Series([1,2,3])",
      convert = FALSE
    )
    pygradethis::py_check_series(.result, .solution)
  })
  testthat::expect_false(check_series_incorrect)
})
