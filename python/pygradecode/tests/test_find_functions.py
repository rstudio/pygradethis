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
  
  elements_source = found.extract_elements()
  expected_source = ['sum', 'sum', 'len']

  assert isinstance(found, GradeCodeFound)
  assert len(found.elements) == 3
  assert all(isinstance(e, Element) for e in found.elements)
  assert elements_source == expected_source

def test_find_functions_nested():
  # nested function calls
  code = 'sum([1, round(2.5), 3])'
  found = find_functions(code)

  elements_source = found.extract_elements()
  expected_source = ['sum', 'round']

  assert isinstance(found, GradeCodeFound)
  assert len(found.elements) == 2
  assert all(isinstance(e, Element) for e in found.elements)
  assert elements_source == expected_source

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
  assert isinstance(found, GradeCodeFound)
  assert len(found.elements) == 0

  # a few lambdas in different forms
  code = 'add_two = lambda x: x + 2\nlambda y: y - 2\n(lambda z: z * 2)(2)'
  found = find_lambdas(code)

  elements_source = found.extract_elements()
  expected_source = ['lambda x: x + 2', 'lambda y: y - 2', 'lambda z: z * 2']

  assert isinstance(found, GradeCodeFound)
  assert len(found.elements) == 3
  assert all(isinstance(e, Element) for e in found.elements)
  assert elements_source == expected_source

def test_uses_lambda():
  code = 'sum([1,2,3])'
  assert uses_lambda(code) is False

  code = 'add_two = lambda x: x + 2'
  assert uses_lambda(code) is True
