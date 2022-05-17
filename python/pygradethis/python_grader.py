"""
This module contains functions to faciliate checking Python code or output.
"""
from typing import Any

from .pygradethis_exercise_checker import pygradethis_exercise_checker
from .conditions import GraderCondition

def grade(
  *check_code: GraderCondition,
  user_code: str = None, 
  solution_code: str = None,
  last_value: Any = None
  ) -> dict:
  """Python standalone verson of `pygradethis_exercise_checker`. This function does
  two things:
  - Do static code grading (AST) if both user and solution code is provided
    before the result grading.
  - Do result grading based on code output and GraderCondition(s)

  Note: Currently, this is just a wrapper around `pygradethis_exercise_checker` and in the
  future we can make changes to handle standalone-specific details.

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
  return pygradethis_exercise_checker(
    user_code = user_code,
    solution_code = solution_code,
    check_code = check_code,
    envir_prep = {},
    envir_result = {}
  )

