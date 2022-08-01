library(reticulate)
library(dplyr)

test_that("Python DataFrame to tibble translation works", {
  # setup Python libraries
  reticulate::py_run_string('import pandas as pd; import numpy as np')

  # no groups
  py_df <- reticulate::py_eval(
    'pd.DataFrame({"Animal": ["Falcon","Falcon","Parrot","Parrot"], "Max Speed": [380., 370., 24., 26.]})', 
    convert = FALSE
  )
  py_tbl_df <- pygradethis::py_to_tbl(py_df)
  expected_tbl <- tibble::tribble(
      ~Animal, ~`Max Speed`,
      "Falcon",   380,
      "Falcon",   370,
      "Parrot",   24,
      "Parrot",   26
  )
  class(expected_tbl) <- append("py_tbl_df", class(expected_tbl))
  testthat::expect_equal(py_tbl_df, expected_tbl)

  # single group
  py_df <- reticulate::py_eval(
    'pd.DataFrame({"Animal": ["Falcon","Falcon","Parrot","Parrot"], "Max Speed": [380., 370., 24., 26.]}).groupby(["Animal"]).mean()', 
    convert = FALSE
  )
  py_tbl_df <- pygradethis::py_to_tbl(py_df)
  expected_tbl <- tibble::tribble(
      ~Animal, ~`Max Speed`,
      "Falcon",   375,
      "Parrot",   25
  ) %>% group_by(Animal)
  class(expected_tbl) <- append(c("py_grouped_df", "py_tbl_df"), class(expected_tbl))
  testthat::expect_equal(py_tbl_df, expected_tbl)

  # multiple groups
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
  py_tbl_df <- pygradethis::py_to_tbl(py_df)
  expected_tbl <- tibble::tribble(
      ~class, ~order, ~max_speed,
      "bird", "Falconiformes", 389.0,
      "bird", "Psittaciformes", 24.0,
      "mammal", "Carnivora", 69.1,
      "mammal", "Primates", NaN
  ) %>% group_by(class, order)
  class(expected_tbl) <- append(c('py_grouped_df', 'py_tbl_df'), class(expected_tbl))
  testthat::expect_equal(py_tbl_df, expected_tbl)
})
