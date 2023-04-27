library(reticulate)

test_that("hinted_class_message() works when expecting a grouped dataframe", {
  pollution <- tibble::tribble(
    ~city,   ~size, ~amount, 
    "New York", "large",      23,
    "New York", "medium",      17, 
    "New York", "small",      14,
    "London", "large",      22,
    "London", "medium",      19,
    "London", "small",      16,
    "Beijing", "large",      121,
    "Beijing", "medium",      73,
    "Beijing", "small",      56
  )
  # we expect same message when if student's dataframe is not grouped 
  # when we expect dataframe outputs from .groupby()/.pivot()/other methods
  expected_message <- "I was only expecting 1 value for each grouping in the table, but you have multiple values per grouping."

  expecting_groupby <- with_py_clear_env({
    py$pollution <- reticulate::r_to_py(pollution)
    .result <- reticulate::py_eval('pollution', convert = FALSE)
    .solution <- reticulate::py_eval('pollution.groupby("city").agg({"amount": "mean"})', convert=FALSE)
    tblcheck::problem_message(pygradethis::py_check_dataframe(.result, .solution))
  })
  expect_equal(
    expecting_groupby,
    expected_message
  )

  expecting_pivot <- with_py_clear_env({
    py$pollution <- reticulate::r_to_py(pollution)
    obj <- pygradethis::py_to_tbl(reticulate::py_eval('pollution', convert = FALSE))
    exp <- pygradethis::py_to_tbl(reticulate::py_eval('
(pollution
  .pivot(
    index = "city",
    columns = "size",
    values = "amount")
)', convert=FALSE))
    tblcheck::hinted_class_message(
      object = obj,
      expected = exp
    )
  })
  expect_equal(
    expecting_pivot,
    expected_message
  )
})