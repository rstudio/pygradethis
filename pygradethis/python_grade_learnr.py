"""
This is the `learnr` version of `python_grader` module and contains
the `python_grade_learnr` function called by the `gradethispython` R wrapper
package
"""
import parser
from typing import Any, Union, Callable, List, Tuple

from .utils import parse_code
from .feedback import praise, encourage
from .grade_result import python_compare_output, python_grade_result

def python_grade_learnr(label: str = None,
                        solution_code: str = None,
                        user_code: str = None,
                        check_code: List[str] = None,
                        envir_result: dict = None,
                        evaluate_result: List[str] = None,
                        envir_prep: dict = None,
                        last_value: Any = None,
                        **kwargs) -> dict:
  """This function mirrors the `grade_learnr` function from {gradethis} package so that
  we can check Python exercises.

  Parameters
  ----------
  label : str, optional
      exercise label, by default None
  solution_code : str, optional
      solution source code, by default None
  user_code : str, optional
      user source code, by default None
  check_code : List[str], optional
      checking code, by default None
  envir_result : dict, optional
      environment containing execution results, by default None
  evaluate_result : List[str], optional
      evaluation results, by default None
  envir_prep : dict, optional
      environment associated with exercise, by default None
  last_value : Any, optional
      the last value of exercise, by default None

  Returns
  -------
  dict
      a feedback dict:
      {
        message = str,
        correct = True|False,
        type = "auto|success|info|warning|error|custom",
        location = "append|prepend|replace"
      }
  """
  # check if there is user_code
  if user_code and "".join(user_code) == "":
    return dict(
      message="I didn't receive your code. Did you write any?",
      correct=False,
      type="error",
      location="append"
    )
  # if there is check code and solution code, check if there is a solution code
  if (check_code and solution_code) and "".join(solution_code) == "":
    return dict(
      message="No solution is provided for this exercise.",
      correct=True,
      type="info",
      location="append"
    )

  # TODO `grade_code(user_code, solution_code)` if solution code is provided

  # evaluate exercise
  try:
    # TODO input scrubbing for malicious code
    check_code_source = parse_code(check_code)
    user_code_source = parse_code(user_code)
    # Note: because Python is eager evaluation, we already have introduced
    # the `r` object in the current scope when entering this function
    # evaluate check code so that expected output is ready
    check_code_conditions = eval(check_code_source, {}, r)
    # for e.g. did knitr already execute result and it's somewhere in the `r`?
    # evaluate user code so that we can compare to expected
    user_result = eval(user_code_source, {}, r)
    # grade python_pass_if/fail_if conditions against user's code output
    result, condition = python_grade_result(check_code_conditions, user_result = user_result)
  except Exception as e:
    # TODO somehow trickle up the specific error message?
    return dict(
      message=f"Error occured while checking the submission: {e}",
      correct=False,
      type="warning",
      location="append"
    )
  # return a list representing a dict condition for learnr to process for feedback
  if (result and condition):
    # correct
    if condition['correct']:
      return dict(
        message = f"{praise()} {condition['message']}", 
        correct = True,
        type = "success", 
        location = "append"
      )
    # incorrect
    return dict(
      message = f"{encourage()} {condition['message']}",
      correct = False,
      type = "error", 
      location = "append"
    )
  # if there was none of the conditions matched, return error by default
  elif not result and not condition:
    return dict(
      message = f"{encourage()}", 
      correct = False, 
      type = "error", 
      location = "append"
    )
  # if there were fail_ifs and none matched, return success by default
  elif result and not condition:
    return dict(
      message = f"{praise()}",
      correct = True,
      type = "success", 
      location = "append"
    )
  else:
    return dict(
      message = f"{encourage()} {condition['message']}", 
      correct = False, 
      type = "error", 
      location = "append"
    )
