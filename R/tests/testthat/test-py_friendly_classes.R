# test_that("friendly_class() for no objects returned", {
#   # Note: this is emulating what happens when there are no objects being returned
#   # in an exercise, where learnr will return placeholder string
#   last_value <- reticulate::py_eval("'__reticulate_placeholder__'", convert=FALSE)
#   last_value <- pygradethis::py_to_r(last_value)
#   print(friendly_class(
#       last_value
#   ))

#   expect_equal(
#     friendly_class(
#       last_value
#     ),
#     "`None`. Did you remember to return an object?"
#   )
# })

# test_that("friendly_class() None", {
#   py_envir <- reticulate::py_eval("{}", convert=FALSE)
#   last_value <- pygradethis::py_to_r(
#     reticulate::py_eval("None", convert=FALSE)
#   )
#   expect_equal(
#     friendly_class(
#       last_value
#     ),
#     "an object with class `None`"
#   )
# })

test_that("friendly_class() int", {
  expect_equal(
    friendly_class(
      pygradethis::py_to_r(reticulate::py_eval("1", convert=FALSE))
    ),
    "an integer (class `int`)"
  )
})

test_that("friendly_class() float", {
  expect_equal(
    friendly_class(
      pygradethis::py_to_r(reticulate::py_eval("1.0", convert=FALSE))
    ),
    "a floating point number (class `float`)"
  )
})

test_that("friendly_class() complex", {
  expect_equal(
    friendly_class(
      pygradethis::py_to_r(reticulate::py_eval("complex(1,1)", convert=FALSE))
    ),
    "a complex number (class `complex`)"
  )
})

test_that("friendly_class() bool", {
  expect_equal(
    friendly_class(
      pygradethis::py_to_r(reticulate::py_eval("True", convert=FALSE))
    ),
    "a boolean (class `bool`)"
  )
})

test_that("friendly_class() str", {
  expect_equal(
    friendly_class(
      pygradethis::py_to_r(reticulate::py_eval("'string'", convert=FALSE))
    ),
    "a string (class `str`)"
  )
})

test_that("friendly_class() tuple", {
  expect_equal(
    friendly_class(
      pygradethis::py_to_r(reticulate::py_eval("(1, 2)", convert=FALSE))
    ),
    "a tuple (class `tuple`)"
  )
})

test_that("friendly_class() set", {
  expect_equal(
    friendly_class(
      pygradethis::py_to_r(reticulate::py_eval("{1, 2}", convert=FALSE))
    ),
    "a set (class `set`)"
  )
})

test_that("friendly_class() dict", {
  expect_equal(
    friendly_class(
      pygradethis::py_to_r(reticulate::py_eval("{'a': 1}", convert=FALSE))
    ),
    "a dictionary (class `dict`)"
  )
})
