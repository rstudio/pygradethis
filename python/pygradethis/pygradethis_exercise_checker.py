"""
This is the `learnr` version of `python_grader` module and contains
the `pygradethis_exercise_checker` function called by the `gradethispython` R wrapper
package
"""
from copy import copy
from typing import Any, Union, List, Tuple

from .grade_result import grade_result
from .grade_code import grade_code
from .conditions import *
from .feedback import praise, encourage
from .utils import parse_code

def graded(graded: Union[str, dict]):
  if (graded is not None):
    correct = graded['correct']
    # correct
    if correct:
      return dict(
        message = "{} {}".format(praise(), graded['message']),
        correct = True,
        type = "success", 
        location = "append"
      )
    # incorrect
    return dict(
      message = "{} {}".format(encourage(), graded['message']),
      correct = False,
      type = "error", 
      location = "append"
    )
  # if there was none of the conditions matched, return error by default
  elif not graded:
    return dict(
      message = "{}".format(encourage()), 
      correct = False, 
      type = "error",
      location = "append"
    )

def pygradethis_exercise_checker(label: str = None,
                        solution_code: str = None,
                        user_code: str = None,
                        check_code: List[str] = None,
                        envir_result: dict = {},
                        evaluate_result: List[str] = [],
                        envir_prep: dict = {},
                        last_value: Any = None) -> dict:
  """This function mirrors the `grade_learnr` function from {gradethis} package so that
  we can check Python exercises. This function does two things:
  - Do static code grading (AST) if both user and solution code is provided
    before the result grading.
  - Do result grading based on code output and Graded(s)

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

  # TODO validate checking code after the final check source is constructed
  # the final checking code includes the grading modules and stores the final grade in
  # a variable that we can reference later
  final_check_source = f"__result__ = {check_code}"
  
  # prep the dictionary that will hold imports, the variables passed into this function, and 
  # everything else that learnr stored into `envir_prep`
  # NOTE: in the future, we could abstract and have an Exercise class that would have envir bits 
  # and could have functions to do the checking + check flows
  if envir_prep is not None:
    graded_envir = dict(globals(), **locals(), **envir_prep)
  else:
    graded_envir = dict(globals(), **locals())
  graded_envir = {k: v for k, v in graded_envir.items() if v is not None}

  # evaluate exercise and check code output
  try:
    # NOTE: eventually this will have to follow the gradethis grading flow where check code
    # can either contain the grading the result or the code and use the student's result
    # evaluate check code and return the result and a Graded list structure
    exec(final_check_source, graded_envir)
    # extract the result out of the environment
    result = graded_envir['__result__']
  except Exception as e:
    # TODO somehow trickle up the specific error message?
    return dict(
      message="Error occured while checking the submission. {}".format(str(e)),
      correct=False,
      type="warning",
      location="append"
    )
  # return a dict for learnr to process for feedback
  return graded(result)
