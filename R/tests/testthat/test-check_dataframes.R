
### Checking ----

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
  testthat::expect_null(check_index_correct)

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
  testthat::expect_true(is_pygradethis_problem(check_index_incorrect))
  testthat::expect_equal(check_index_incorrect$type, "wrong_index")
})

test_that("py_check_columns() works on DataFrame without column Index", {
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
  testthat::expect_null(check_columns_correct)

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
  testthat::expect_true(is_pygradethis_problem(check_columns_incorrect))
  testthat::expect_equal(check_columns_incorrect$type, "wrong_columns")
})

test_that("py_check_columns() ignores columns with an Index", {
  check_columns_incorrect <- callr::r_safe(function() {
    library(reticulate)
    reticulate::py_run_string('import pandas as pd; import numpy as np')
    .result <- reticulate::py_eval(
      "pd.DataFrame({'a':[1,2,3]}, index = ['A', 'B', 'C'])",
      convert = FALSE
    )
    .solution <- reticulate::py_eval(
      "pd.DataFrame({'a':[1,2,3]}, index = ['C', 'B', 'A'])",
      convert = FALSE
    )
    pygradethis::py_check_columns(.result, .solution)
  })
  testthat::expect_null(check_columns_incorrect)
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
  testthat::expect_null(check_values_correct)

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
  testthat::expect_true(is_pygradethis_problem(check_values_incorrect))
  testthat::expect_equal(check_values_incorrect$type, "wrong_values")
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

  check_dataframe_incorrect <- callr::r_safe(function() {
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
  testthat::expect_true(tblcheck::is_tblcheck_problem(check_dataframe_incorrect))
  testthat::expect_equal(check_dataframe_incorrect$type, "names")
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
  testthat::expect_null(check_series_correct)

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
  testthat::expect_true(is_pygradethis_problem(check_series_incorrect))
  testthat::expect_equal(check_series_incorrect$type, "wrong_series")
})

### Grading ----

test_that("py_grade_index() works on DataFrame with no Index", {
  grade_index_correct <- callr::r_safe(function() {
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
    pygradethis::py_grade_index(.result, .solution)
  })
  testthat::expect_null(grade_index_correct)

  grade_index_incorrect <- callr::r_safe(function() {
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
    pygradethis::py_grade_index(.result, .solution)
  })
  testthat::expect_true(inherits(grade_index_incorrect, c("gradethis_graded", "condition")))
  testthat::expect_false(grade_index_incorrect$correct)
})

test_that("py_grade_index() works on DataFrame with an Index", {
  grade_index_correct <- callr::r_safe(function() {
    library(reticulate)
    reticulate::py_run_string('import pandas as pd; import numpy as np')
    .result <- py_eval('pd.DataFrame(np.random.randn(3, 8), index=["A", "B", "C"])')
    .solution <- py_eval('pd.DataFrame(np.random.randn(3, 8), index=["A", "B", "C"])')
    pygradethis::py_grade_index(.result, .solution)
  })
  testthat::expect_null(grade_index_correct)

  grade_index_incorrect <- callr::r_safe(function() {
    library(reticulate)
    reticulate::py_run_string('import pandas as pd; import numpy as np')
    .result <- py_eval('pd.DataFrame(np.random.randn(3, 8), index=["A", "B", "C"])')
    .solution <- py_eval('pd.DataFrame(np.random.randn(3, 8), index=["C", "B", "A"])')
    pygradethis::py_grade_index(.result, .solution)
  })
  testthat::expect_true(inherits(grade_index_incorrect, c("gradethis_graded", "condition")))
  testthat::expect_false(grade_index_incorrect$correct)
})

test_that("py_grade_columns() works on DataFrame columns", {
  grade_columns_correct <- callr::r_safe(function() {
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
    pygradethis::py_grade_columns(.result, .solution)
  })
  testthat::expect_null(grade_columns_correct)

  # we currently ignore Index
  grade_columns_correct <- callr::r_safe(function() {
    library(reticulate)
    reticulate::py_run_string('import pandas as pd; import numpy as np')
    .result <- reticulate::py_eval(
      "pd.DataFrame({'a':[1,2,3]}, index = ['A', 'B', 'C'])",
      convert = FALSE
    )
    .solution <- reticulate::py_eval(
      "pd.DataFrame({'a':[1,2,3]}, index = ['C', 'B', 'A'])",
      convert = FALSE
    )
    pygradethis::py_grade_columns(.result, .solution)
  })
  testthat::expect_null(grade_columns_correct)

  grade_columns_incorrect <- callr::r_safe(function() {
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
    pygradethis::py_grade_index(.result, .solution)
  })
  testthat::expect_true(inherits(grade_columns_incorrect, c("gradethis_graded", "condition")))
  testthat::expect_false(grade_columns_incorrect$correct)
})

test_that("py_grade_columns() works on MultiIndex columns", {
  grade_columns_correct <- callr::r_safe(function() {
    library(reticulate)
    reticulate::py_run_string('import pandas as pd; import numpy as np')
    py_env <- reticulate::py_run_string('
arrays = [
  np.array(["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"]),
  np.array(["one", "two", "one", "two", "one", "two", "one", "two"]),
]
tuples = list(zip(*arrays))
index = pd.MultiIndex.from_tuples(tuples, names=["first", "second"])
correct = pd.DataFrame(np.random.randn(3, 8), index=["A", "B", "C"], columns=index)
incorrect = pd.DataFrame(np.random.randn(3, 8), index=["A", "B", "C"], columns=index)
')
    .result <- py_eval('correct')
    .solution <- py_eval('incorrect')
    pygradethis::py_grade_columns(.result, .solution)
  })
  testthat::expect_null(grade_columns_correct)

  grade_columns_incorrect <- callr::r_safe(function() {
    library(reticulate)
    reticulate::py_run_string('import pandas as pd; import numpy as np')
    py_env <- reticulate::py_run_string('
arrays = [
  np.array(["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"]),
  np.array(["one", "two", "one", "two", "one", "two", "one", "two"]),
]
tuples = list(zip(*arrays))
index = pd.MultiIndex.from_tuples(tuples, names=["first", "second"])
correct = pd.DataFrame(np.random.randn(3, 8), index=["A", "B", "C"], columns=index)
incorrect = pd.DataFrame(np.random.randn(3, 8), index=["A", "B", "C"])
')
    .result <- py_eval('correct')
    .solution <- py_eval('incorrect')
    pygradethis::py_grade_columns(.result, .solution)
  })
  testthat::expect_true(inherits(grade_columns_incorrect, c("gradethis_graded", "condition")))
  testthat::expect_false(grade_columns_incorrect$correct)
})