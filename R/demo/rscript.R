reticulate::use_virtualenv("~/.virtualenvs/pygradethis")
library(pygradethis)

exercise_checker(
    label = "dan-python-test",
    solution_code = "3",
    user_code = "3",
    check_code = 'python_grade_result(
    python_pass_if(3, "You wrote the add!"),
    python_fail_if(None, ""),
    user_result = 3
  )'
)
