"""
This module contains functions to faciliate checking Python code or output.
"""
from typing import Union

from .grade_result import python_grade_result
from .grade_code import grade_code
from .conditions import GraderCondition
from .feedback import praise, encourage
from .utils import parse_code

def graded(result: Union[str, dict], condition: GraderCondition, unittest_style: bool = False):
  # return a dict for feedback
  if unittest_style:
    num_correct = condition['num_correct']
    total = condition['total']
    message = condition['message'].format(num_correct, total)
    type = "success" if num_correct == total else "error"
    return dict(
      message = message,
      num_correct = num_correct,
      type = type
    )
  if result and condition:
    # correct
    if condition['correct']:
      return dict(
        message = "{} {}".format(praise(), condition['message']), 
        correct = True,
        type = "success"
      )
    # incorrect
    return dict(
      message = "{} {}".format(encourage(), condition['message']),
      correct = False,
      type = "error"
    )
  # if none of the conditions matched, return incorrect by default
  elif not result and not condition:
    return dict(
      message = "{}".format(encourage()), 
      correct = False, 
      type = "error"
    )
  # if there were fail_ifs and none matched, return success by default
  elif result and not condition:
    return dict(
      message = "{}".format(praise()),
      correct = True,
      type = "success"
    )
  else:
    return dict(
      message = "{} {}".format(encourage(), condition['message']), 
      correct = False, 
      type = "error"
    )


def grade(
  *check_code: GraderCondition,
  user_code: str = None, 
  solution_code: str = None,
  unittest_style = False
  ) -> dict:
  """Python standalone verson of `python_grade_learnr`. This function does
  two things:
  - Do static code grading (AST) if both user and solution code is provided
    before the result grading.
  - Do result grading based on code output and GraderCondition(s)

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
    
  # TODO input scrubbing for malicious code
  # parse user, and solution code
  solution_code = parse_code(solution_code)
  user_code_source = parse_code(user_code)
  if solution_code is not None:
    # do static checks on code if the solution code is provided
    graded_code = grade_code(user_code_source, solution_code)
    if graded_code is not None:
      return dict(
        message = "{}".format(graded_code),
        correct = False,
        type = "error", 
      )

  # evaluate exercise and check code output
  try:
    # evaluate user code so that we can compare to expected
    user_result = eval(user_code_source)
  except Exception as e:
    # TODO somehow trickle up the specific error message?
    return dict(
      message="Error occured while checking the submission. {e}".format(e),
      correct = False, 
      type = "warning"
    )

  # grade python_pass_if/fail_if conditions against user's code output
  result, condition = python_grade_result(*check_code, user_result = user_result, unittest_style = unittest_style)
  # return a graded dict
  return graded(result = result, condition = condition, unittest_style = unittest_style)

