import pygradethis
from pygradethis.pygradethis_exercise_checker import pygradethis_exercise_checker

check_code = (
"""grade_result(
    pass_if_equals(6, 'You wrote the add!'),
    fail_if_equals(None, 'Oops!'),
    user_result = last_value
)
"""
)

print(
    pygradethis_exercise_checker(solution_code = "3 + 3", user_code = "3 + 3", check_code = check_code, last_value = 6)
)