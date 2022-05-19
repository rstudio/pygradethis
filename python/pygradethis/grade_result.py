"""
This module is used to check python code output.
"""

from typing import Any, Union, List

from .conditions import GraderCondition
from .result_checker import test_conditions

# TODO add the glue type messages to construct custom messages
# glue_correct = getOption("gradethis_glue_correct"),
# glue_incorrect = getOption("gradethis_glue_incorrect")
def grade_result(
    *conditions: List[GraderCondition], 
    user_result: Any = None
  ) -> Union[dict, str]:
  """This function checks the user's code output against the list of conditions.

  Parameters
  ----------
  conditions: *GraderCondition
      a variable number of GraderCondition objects
  user_result : Any, optional
      user's code output, by default None

  Returns
  -------
  Union[dict, str]
      dict, if there are no issues
      str, an error message if GraderCondition(s) is not supplied

  Raises
  ------
  Exception
      if GraderConditions are not passed in for conditions
  """
  all_conditions = [c for c in conditions if isinstance(c, GraderCondition)]
  if conditions == None or len(all_conditions) == 0:
    raise Exception(
      "At least one condition object (e.g., `pass_if_equals()`, "
      "`fail_if_equals()`, `python_condition()`) must be provided to"
      "`grade_result()`"
    )
  if user_result is not None:
    return test_conditions(*conditions, user_result = user_result)
  return conditions
