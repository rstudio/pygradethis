reticulate::use_virtualenv("~/.venvs/pygradethis")
library(learnr)
library(pygradethis)
library(reticulate)

duplicate_py_env <- function(module) {
  # list objects within this module
  new_objs <- reticulate::py_get_attr(module, "__dict__")
  # create copy of dictionary
  copy <- reticulate::import("copy", convert = FALSE)
  copy$copy(new_objs)
}

# store the `py` to access `x` when grading
# 1) first store the envir_prep that's a duplicate of global
envir_prep <- learnr:::duplicate_env(globalenv())

paste0(c("envir_prep before: ", names(envir_prep)), collapse = " ")

# 2) run setup code
# reticulate::py_run_string("import pandas")
reticulate::py_run_string("x = 3")

# 3) copy the `envir_prep`
envir_prep <- duplicate_py_env(py) # the `py` module can be accessed in Python side!

# check `envir_prep` after
paste0(c("envir_prep after: ", names(envir_prep)), collapse = " ")

# then save the new `py` into envir_result
reticulate::py_run_string("y = x + 3")

paste0(c("envir_result before: ", names(envir_result)), collapse = " ")

envir_result <- duplicate_py_env(py)

paste0(c("envir_result after: ", names(envir_result)), collapse = " ")

# these should look different now
names(envir_prep)
names(envir_result)

# 4) run exercise code
exercise_checker(
    label = "dan-python-test",
    solution_code = "3",
    user_code = "3",
    check_code = 'python_grade_result(
    python_pass_if(3, "You wrote the add!"),
    python_fail_if(None, ""),
    user_result = last_value
  )',
  envir_prep = envir_prep,
  envir_result = envir_result,
  last_value = 3
)
