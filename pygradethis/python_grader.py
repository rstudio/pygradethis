"""
This module contains functions to faciliate checking Python code or output.
"""

import parser
from typing import Any, Callable, List, Tuple

from .conditions import GraderCondition
from .feedback import praise, encourage
from .grade_result import python_grade_result
from .utils import parse_code

# TODO refactor for Python standalone
def grade(*check_code: GraderCondition,
          user_code: str = None, 
          solution_code: str = None) -> dict:
  """Python standalone verson of `python_grade_learnr`.

  Parameters
  ----------
  check_code: *GraderCondition
      a variable number of GraderCondition objects
  user_code : str, optional
      user source code, by default None
  solution_code : str, optional
      solution source code, by default None

  Returns
  -------
  dict
      a feedback dict:
      {
        message: str,
        correct=True|False,
        type="auto|success|info|warning|error|custom",
        location="append|prepend|replace"
      }
  """
  # check if there is user_code
  if user_code and "".join(user_code) == "":
    return dict(
      message = "I didn't receive your code. Did you write any?",
      correct = False,
      type = "error"
    )
  # if there is check code and solution code, check if there is a solution code
  if (check_code and solution_code) and "".join(solution_code) == "":
    return dict(
      message = "No solution is provided for this exercise.",
      correct = True,
      type = "info"
    )
  
  # TODO `grade_code(user_code, solution_code)` if solution code is provided


  # evaluate exercise
  try:
    # TODO input scrubbing for malicious code
    # attempt to parse and format code
    user_code_source = parse_code(user_code)
    # evaluate user code so that we can compare to expected
    user_result = eval(user_code_source)
  except Exception as e:
    # TODO somehow trickle up the specific error message?
    return dict(
      correct = False, 
      message = f"Error occured while checking the submission {e}", 
      type = "warning"
    )

  # print(check_code, type(check_code))
  # grade python_pass_if/fail_if conditions against user's code output
  result, condition = python_grade_result(*check_code, user_result = user_result)
  # return a list representing a dict condition for learnr to process for feedback
  if (result and condition):
    # correct
    if condition['correct']:
      return dict(
        message = f"{praise()} {condition['message']}", 
        correct = True,
        type = "success"
      )
    # incorrect
    return dict(
      message = f"{encourage()} {condition['message']}",
      correct = False,
      type = "error"
    )
  # if there was none of the conditions matched, return error by default
  elif not result and not condition:
    return dict(
      message = f"{encourage()}", 
      correct = False, 
      type = "error"
    )
  # if there were fail_ifs and none matched, return success by default
  elif result and not condition:
    return dict(
      message = f"{praise()}",
      correct = True,
      type = "success"
    )
  else:
    return dict(
      message = f"{encourage()} {condition['message']}", 
      correct = condition['correct'], 
      type = "error"
    )
  

