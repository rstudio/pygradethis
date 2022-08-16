library(dplyr)

test_that("py_to_r() translates DataFrames", {
  # NOTE: to be safe, we isolate reticulate calls to a fresh R process
  py_tbl_df <- callr::r_safe(function() {
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
  py_series <- callr::r_safe(function() {
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
  py_multi_index <- callr::r_safe(function() {
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
  py_tbl_df <- callr::r_safe(function() {
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
  py_tbl_df <- callr::r_safe(function() {
    library(reticulate)
    reticulate::py_run_string('import pandas as pd; import numpy as np')
    py_df <- reticulate::py_eval(
      'pd.DataFrame({"Animal": ["Falcon","Falcon","Parrot","Parrot"], "Max Speed": [380., 370., 24., 26.]}).groupby(["Animal"]).mean()', 
      convert = FALSE
    )
    pygradethis::py_to_tbl(py_df)
  })
  expected_tbl <- tibble::tribble(
      ~Animal, ~`Max Speed`,
      "Falcon",   375,
      "Parrot",   25
  ) %>% group_by(Animal)
  class(expected_tbl) <- c("py_grouped_df", "py_tbl_df", class(expected_tbl))
  testthat::expect_equal(py_tbl_df, expected_tbl)
})

testthat::test_that("py_to_tbl() translates DataFrame to tibble with multiple groups", {
  py_tbl_df <- callr::r_safe(function() {
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
  ) %>% group_by(class, order)
  class(expected_tbl) <- c('py_grouped_df', 'py_tbl_df', class(expected_tbl))
  testthat::expect_equal(py_tbl_df, expected_tbl)
})
