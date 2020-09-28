"""
This is the `learnr` version of `python_grader` module and contains
the `python_grade_learnr` function called by the `gradethispython` R wrapper
package
"""
import parser
from typing import Any, Union, List, Tuple

from .grade_result import python_grade_result
from .grade_code import grade_code
from .conditions import GraderCondition
from .feedback import praise, encourage
from .utils import parse_code

def graded_learnr(result: Union[str, dict], condition: GraderCondition):
  if (result and condition):
    # correct
    if condition['correct']:
      return dict(
        message = "{} {}".format(praise(), condition['message']), 
        correct = True,
        type = "success", 
        location = "append"
      )
    # incorrect
    return dict(
      message = "{} {}".format(encourage(), condition['message']),
      correct = False,
      type = "error", 
      location = "append"
    )
  # if there was none of the conditions matched, return error by default
  elif not result and not condition:
    return dict(
      message = "{}".format(encourage()), 
      correct = False, 
      type = "error", 
      location = "append"
    )
  # if there were fail_ifs and none matched, return success by default
  elif result and not condition:
    return dict(
      message = "{}".format(praise()),
      correct = True,
      type = "success", 
      location = "append"
    )
  else:
    return dict(
      message = "{} {}".format(encourage(), condition['message']), 
      correct = False, 
      type = "error", 
      location = "append"
    )

def python_grade_learnr(label: str = None,
                        solution_code: str = None,
                        user_code: str = None,
                        check_code: List[str] = None,
                        envir_result: dict = None,
                        evaluate_result: List[str] = None,
                        envir_prep: dict = None,
                        last_value: Any = None) -> dict:
  """This function mirrors the `grade_learnr` function from {gradethis} package so that
  we can check Python exercises. This function does two things:
  - Do static code grading (AST) if both user and solution code is provided
    before the result grading.
  - Do result grading based on code output and GraderCondition(s)

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

  # TODO input scrubbing for malicious code
  # parse user, check and solution code
  solution_code = parse_code(solution_code)
  check_code_source = parse_code(check_code)
  user_code_source = parse_code(user_code)

  # do static checks on code if the solution code is provided
  graded_code = grade_code(user_code_source, solution_code)
  if graded_code is not None:
    return dict(
      message = "{}".format(graded_code),
      correct = False,
      type = "error", 
      location = "append"
    )

  # evaluate exercise and check code output
  try:
    # NOTE: the `r` comes from the explicit import when loading this module
    # via reticulate
    # evaluate check code so that expected output is ready
    check_code_conditions = eval(check_code_source, {}, r)
    # for e.g. did knitr already execute result and it's somewhere in the `r`?
    # evaluate user code so that we can compare to expected
    user_result = eval(user_code_source, {}, r)

    # grade python_pass_if/fail_if conditions against user's code output
    result, condition = python_grade_result(*check_code_conditions, user_result = user_result)
  except Exception as e:
    # TODO somehow trickle up the specific error message?
    return dict(
      message="Error occured while checking the submission. {}".format(str(e)),
      correct=False,
      type="warning",
      location="append"
    )
  # return a dict for learnr to process for feedback
  return graded_learnr(result, condition)

if __name__ != '__main__':
  try:
    # attempt to import if used with R's `learnr` package
    from __main__ import r
  except:
    pass
