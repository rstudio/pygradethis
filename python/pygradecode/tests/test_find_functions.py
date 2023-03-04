from lxml.etree import _Element as Element

from pygradecode.find_functions import (
  find_functions, uses_function, 
  find_lambdas, uses_lambda
)
from pygradecode.grade_code_found import GradeCodeFound

def test_find_functions_simple():
  # function calls that are not nested
  code = 'sum([1,2,3])\nsum([4,5,6])\nlen([1,2,3])'
  found = find_functions(code)
  
  state = found.get_last_state()
  last_result = state.result

  assert isinstance(found, GradeCodeFound)
  assert len(last_result) == 3
  assert all(isinstance(e, Element) for e in last_result)
  assert state.type == 'functions'

def test_find_functions_nested():
  # nested function calls
  code = 'sum([1, round(2.5), 3])'
  found = find_functions(code)

  state = found.get_last_state()
  last_result = state.result

  assert isinstance(found, GradeCodeFound)
  assert len(last_result) == 2
  assert all(isinstance(e, Element) for e in last_result)
  assert state.type == 'functions'

def test_uses_function():
  code = 'sum([1,2,3])'

  assert uses_function(code, 'sum') is True
  assert uses_function(code, 'round') is False

  # nested function works as well
  code = 'sum([1, round(2.5), 3])'
  assert uses_function(code, 'sum') is True
  assert uses_function(code, 'round') is True

def test_find_lambdas():
  # no lambdas
  code = 'def add_two(x):\n  return x + 2'
  found = find_lambdas(code)

  state = found.get_last_state()
  last_result = found.last_result

  assert isinstance(found, GradeCodeFound)
  assert len(last_result) == 0
  assert state.type == 'lambdas'

  # a few lambdas in different forms
  code = 'add_two = lambda x: x + 2\nlambda y: y - 2\n(lambda z: z * 2)(2)'
  found = find_lambdas(code)

  state = found.get_last_state()
  last_result = found.last_result

  assert isinstance(found, GradeCodeFound)
  assert len(last_result) == 3
  assert all(isinstance(e, Element) for e in last_result)
  assert state.type == 'lambdas'

def test_uses_lambda():
  code = 'sum([1,2,3])'
  assert uses_lambda(code) is False

  code = 'add_two = lambda x: x + 2'
  assert uses_lambda(code) is True
