"""
This module contains functions to faciliate checking Python code or output.
"""

import parser
from typing import Any, Union, Callable, List, Tuple

# TODO refactor for Python standalone
def grade(user_code: str = None, 
          solution_code: str = None, 
          checking: Union[str, GraderCondition] = None) -> Graded:
  """Python standalone verson of `python_grade_learnr`.

  Parameters
  ----------
  user_code : str, optional
      the user source text, by default None
  solution_code : str, optional
      the solution source text, by default None
  checking : GraderCondition, optional
      checking code represented, by default None

  Returns
  -------
  Graded
      a convenience class to represent graded code / output
  """
  # check if there is user_code
  if user_code and "".join(user_code) == "":
    return Graded(
      message = "I didn't receive your code. Did you write any?",
      correct = False,
      type = "error",
      location = "append"
    )
  # if there is check code and solution code, check if there is a solution code
  if (check_code and solution_code) and "".join(solution_code) == "":
    return Graded(
      message = "No solution is provided for this exercise.",
      correct = True,
      type = "info",
      location = "append"
    )
  
  # TODO `grade_code(user_code, solution_code)` if solution code is provided
  
  check_code_source = "".join(check_code)
  user_code_source = "\n".join(user_code)

  # TODO we won't need to use r anywhere
  # evaluate exercise
  try:
    # TODO input scrubbing for malicious code
    # Note: because Python is eager evaluation, we already have introduced
    # the `r` object in the current scope when entering this function
    # evaluate check code so that expected output is ready
    check_code_conditions = exec(check_code_source, {}, r)
    # for e.g. did knitr already execute result and it's somewhere in the `r`?
    # evaluate user code so that we can compare to expected
    user_result = exec(user_code_source, {}, r)
  except Exception as e:
    # TODO somehow trickle up the specific error message?
    return Graded(
      correct = False, 
      message = f"Error occured while checking the submission {e}", 
      type = "warning", 
      location = "append",
      check_code = f"{check_code_source}",
      user_code = f"{user_code_source}",
    )

  # TODO fix when we don't get a tuple back
  # grade python_pass_if/fail_if conditions against user's code output
  result, condition = python_grade_result(check_code_conditions, user_result)
  # return a list representing a graded condition for learnr to process for feedback
  if result and condition:
    return Graded(
      message = f"{praise()} {condition['message']}", 
      correct = condition['correct'], 
      type = "success", 
      location = "append"
    )
  elif not result and not condition:
    return Graded(
      message = f"{encourage()}", 
      correct = False, 
      type = "success", 
      location = "append"
    )
  else:
    return Graded(
      message = f"{encourage()} {condition['message']}", 
      correct = condition['correct'], 
      type = "error", 
      location = "append"
    )
  

