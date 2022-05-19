reticulate::use_virtualenv("~/.venvs/pygradethis")
library(pygradethis)

pygradethis::exercise_checker(
  label = "sum-ex",
  solution_code = "3 + 3",
  user_code = "3 + 3",
  check_code = 'grade_result(
  pass_if_equals(6, "You wrote the add!"),
  fail_if_equals(message = ""),
  user_result = 6
)'
)
