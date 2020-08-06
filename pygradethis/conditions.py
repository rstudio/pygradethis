
import pandas as pd

class GraderCondition(dict):
    """Convience class to represent the a grader condition for an exercise.
    
    Note: we subclass a `dict` for the same reason as `dict`
    
    Returned `dict` is equivalent to the `list` returned in `gradethis::condition`
    
    Example:
    
    GraderCondition(
      x = x,
      message = message,
      correct = correct,
      type = type
    )
    """
    def __init__(self, *args, **kwargs):
      # TODO validation of kwargs to only accept the valid names
      super(GraderCondition, self).__init__(kwargs)

def python_condition(x: Any, message: str, correct: bool, type: str = "value") -> dict:
  """Return the proper structure for a particular type of condition."""
  # Note: we don't use the type field from `gradethis::condition` yet, so assumes value
  # TODO think about whether we allow passing of a function (lambda or regular)
  return GraderCondition(x = x, message = message, correct = correct, type = type)

def python_pass_if(x: Any, message = "") -> dict:
  """Return a pass condition."""
  return python_condition(x, message, correct = True)

def python_fail_if(x: Any, message = "") -> dict:
  """Return a fail condition."""
  return python_condition(x, message, correct = False)
  
def python_grade_conditions(conditions: List[Any], user_result: Any) -> Tuple[bool, GraderCondition]:
  """Goes through all conditions (python_pass_if, python_fail_if) and
  returns the first condition that comes True.

  Parameters
  ----------
  conditions : List[Any]
      [description]
  user_result : Any
      [description]

  Returns
  -------
  Tuple[bool, GraderCondition]
      bool is True if user_result is correct, else False
      GraderCondition that matched with the user_result
  """
  # TODO handle the case where you might only have fail_ifs but they don't match (issue #4)
  result = False
  condition = None
  for cond in conditions:
    condition = cond
    result = python_compare_output(cond['x'], user_result)
    if result:
      return result, condition
  # If there is at least one pass_if() condition, then default to an incorrect grade;
  # otherwise, we default to a correct grade https://github.com/rstudio-education/gradethis/issues/118
  if len([c for c in conditions if c['correct']]) != 0:
    return False, None
  return False, None

