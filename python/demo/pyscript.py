from pygradethis.python_grade_learnr import python_grade_learnr

check_code = (
"""
python_grade_result(
    python_pass_if(6, 'You wrote the add!'),
    python_fail_if(None, 'Oops!'),
    user_result = 6
)
"""
)

print(
    python_grade_learnr(label = "dan-python-test", solution_code = "3 + 3", user_code = "3 + 3", check_code = check_code)
)