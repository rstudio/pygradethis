
from typing import Any, List, Tuple

class GraderCondition(dict):
    """Convience class to represent the a grader condition for an exercise.
    
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
