"""
This is the `learnr` version of `python_grader` module and contains 
the `python_grade_learnr` function called by the `gradethispython` R wrapper
package
"""
import parser
from typing import Any, Union, Callable, List, Tuple

def python_grade_learnr(label: str = None,
                        solution_code: str = None, 
                        user_code: str = None, 
                        check_code: List[str] = None, 
                        envir_result: dict = None, 
                        evaluate_result: List[str] = None,
                        envir_prep: dict = None, 
                        last_value: Any = None, 
                        **kwargs) -> dict:
    """
    This function mirrors the `grade_learnr` function from {gradethis} package so that
    we can check Python exercises.
    """
    # check if there is user_code
    if user_code and "".join(user_code) == "":
      return dict(
        message = "I didn't receive your code. Did you write any?",
        correct = False,
        type = "error",
        location = "append"
      )
    # if there is check code and solution code, check if there is a solution code
    if (check_code and solution_code) and "".join(solution_code) == "":
      return dict(
        message = "No solution is provided for this exercise.",
        correct = True,
        type = "info",
        location = "append"
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
      # print(python_grade_result(check_code_conditions, user_result))
      result, condition = python_grade_result(check_code_conditions, user_result)
    except Exception as e:
      # TODO somehow trickle up the specific error message?
      return dict(
        message = f"Error occured while checking the submission: {e}", 
        correct = False, 
        type = "warning", 
        location = "append"
      )s
    # return a list representing a dict condition for learnr to process for feedback
    if result and condition:
      return dict(
        message = f"{praise()} {condition['message']}", 
        correct = condition['correct'], 
        type = "success", 
        location = "append"
      )
    elif not result and not condition:
      return dict(
        message = f"{encourage()}", 
        correct = False, 
        type = "success", 
        location = "append"
      )
    else:
      return dict(
        message = f"{encourage()} {condition['message']}", 
        correct = condition['correct'], 
        type = "error", 
        location = "append"
      )
  
if __name__ == '__main__':
  # for now we don't have any additional setup
  pass
else:
  # this import is for the R package `learnr` so that when we use
  # `reticulate::import_from_path` to selectively expose functions, we make
  # sure to also import `r` which normally doesn't get imported since we do
  # not use `reticulate::source`.
  from __main__ import r

