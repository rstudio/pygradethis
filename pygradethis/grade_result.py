"""
This module is used to check python code output.
"""

def python_compare_output(user_output: Any, expected_output: Any) -> bool:
  """Return whether the user output and expected output match"""
  if type(user_output) != type(expected_output):
    return False
  elif isinstance(user_output, pd.DataFrame) and isinstance(expected_output, pd.DataFrame):
      return user_output.equals(expected_output)
  else:
    return user_output == expected_output

# TODO add the other kwargs for this?
# glue_correct = getOption("gradethis_glue_correct"),
# glue_incorrect = getOption("gradethis_glue_incorrect")
def python_grade_result(*conditions: List[GraderCondition], user_result: Any = None) -> Union[dict, str]:
  """This function checks the user's code output against the list of conditions.
  
  It mirrors the `grade_result` function from {gradethis} package so that
  we can check Python exercises.
  
  For now, all it does is to get all of the python_pass_if/fail_if conditions and 
  returning it.

  Parameters
  ----------
  user_result : Any, optional
      user's code output, by default None

  Returns
  -------
  Union[dict, str]
      dict, if there are no issues
      str, an error message if GraderCondition(s) is not supplied
  """
  # print([type(a) for a in args])
  if conditions == None or len([c for c in conditions if isinstance(c, GraderCondition)]) == 0:
    raise Exception(
      "At least one condition object (e.g., `python_pass_if()`, "
      "`python_fail_if()`, `python_condition()`) must be provided to"
      "`python_grade_result()`"
    )
  # TODO handle user_result None case
  return python_grade_conditions(conditions, user_result)

