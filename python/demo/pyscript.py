import pygradethis
from pygradethis.pygradethis_exercise_checker import pygradethis_exercise_checker

check_code = (
"""
grade_result(
    pass_if_equals(6, 'You wrote the add!'),
    fail_if_equals(None, 'Oops!'),
    user_result = 6
)
"""
)

print(
    pygradethis_exercise_checker(label = "dan-python-test", solution_code = "3 + 3", user_code = "3 + 3", check_code = check_code)
)