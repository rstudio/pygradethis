
from typing import Any, List, Tuple

class Graded(dict):
    """Convience class to represent the a grader condition for an exercise.
    
    Example:
    
    Graded(
      x = x,
      message = message,
      correct = correct,
      type = type
    )
    """
    def __init__(self, x: Any, message: str = "", correct: bool = True, type: str = "value"):
      super(Graded, self).__init__({'x': x, 'message': message, 'correct': correct, 'type': type})

def python_condition(x: Any, message: str = "", correct: bool = True, type: str = "value") -> dict:
  """Return the proper structure for a particular type of condition."""
  # Note: we don't use the type field from `gradethis::condition` yet, so assumes value
  # TODO think about whether we allow passing of a function (lambda or regular)
  return Graded(x = x, message = message, correct = correct, type = type)

def pass_if_equals(x: Any = None, message = "") -> dict:
  """Return a pass condition."""
  return Graded(x = x, message = message, correct = True)

def fail_if_equals(x: Any = None, message = "") -> dict:
  """Return a fail condition."""
  return Graded(x = x, message = message, correct = False)
