from textwrap import dedent
from lxml.etree import _Element as Element

from pygradecode.grade_code_found import QueryResult
from pygradecode.find_functions import find_functions
from pygradecode.find_arguments import (
  find_arguments, args, Arg, KWArg
)
from pygradecode.grade_code_found import GradeCodeFound

def test_find_arguments():
  # function calls that are not nested
  code = 'sum([1, round(2.5), 3])\nprint("Hello", "World!", 2.5, sep=", ")'
  found = find_arguments(code)
  
  state = found.get_last_state()
  last_result = state.result

  assert isinstance(found, GradeCodeFound)
  assert state.type == 'arguments'
  assert len(last_result) == 6
  assert all(isinstance(e, Element) for e in last_result)

  # sum() => [1, round(2.5), 3]
  assert last_result[0].tag == 'List'
  # round() => 2.5
  assert last_result[1].tag == 'Constant'
  # print()
  # "Hello", "World!", 2.5
  assert all(r.tag == 'Constant' for r in last_result[2:5])
  # sep=", "
  assert last_result[5].tag == 'keyword'

def test_find_arguments_match_simple():
  code = 'round(2.5)'

  # match 2.5
  found_constant = find_arguments(code, match=args('2.5'))
  state = found_constant.get_last_state()
  last_result = state.result

  assert isinstance(found_constant, GradeCodeFound)
  assert state.type == 'arguments'

  # check results
  assert len(last_result) == 1
  assert last_result[0].tag == 'Constant'

def test_find_arguments_match_complex():
  code = 'sum([1, round(2.5), 3])'

  # match [1, round(2.5), 3]
  found_list = find_arguments(code, match=args('[1, round(2.5), 3]'))
  state = found_list.get_last_state()
  last_result = state.result

  assert isinstance(found_list, GradeCodeFound)
  assert state.type == 'arguments'

  # check results
  assert len(last_result) == 1
  assert isinstance(last_result[0], Element)
  assert last_result[0].tag == 'List'

def test_find_functions_arguments():
  # nested function calls
  user_code = dedent("""
    sum([1, round(2.5), 3])
    print("Hello", "World!", 2.5, sep=", ")
  """).strip()

  found = find_arguments(
    find_functions(user_code, match = 'print'), 
    match = args("2.5")
  )
  state = found.get_last_state()
  results = found.results

  assert isinstance(found, GradeCodeFound)
  assert state.type == 'arguments'
  
  assert len(results) == 2
  assert all(isinstance(r, QueryResult) for r in results)
  
  # first request 
  first_found = results[0]
  assert first_found.type == 'functions'
  assert first_found.request == 'print'
  assert len(first_found.result) == 1
  assert isinstance(first_found.result[0], Element)
  assert first_found.result[0].tag == 'Call'

  # second request 
  second_found = results[1]
  last_result = found.last_result

  assert second_found.type == 'arguments'
  assert len(second_found.result) == 1
  assert isinstance(last_result[0], Element)
  assert last_result[0].tag == 'Constant'

def test_find_arguments_match_keyword_string():
  code = 'print("Hello", "World!", sep=", ")'

  # match sep=", "
  found_keyword = find_arguments(code, match=args(sep='", "'))
  state = found_keyword.get_last_state()
  last_result = state.result

  assert isinstance(found_keyword, GradeCodeFound)
  assert state.type == 'arguments'

  # check results
  assert len(last_result) == 1
  assert isinstance(last_result[0], Element)
  assert last_result[0].tag == 'Constant'

def test_find_arguments_match_keyword_constant():
  code = 'pow(38, -1, mod=97)'

  # match mod=97
  found_keyword = find_arguments(code, match=args(mod='97'))
  state = found_keyword.get_last_state()
  last_result = state.result

  assert isinstance(found_keyword, GradeCodeFound)
  assert state.type == 'arguments'

  # check results
  assert len(last_result) == 1
  assert isinstance(last_result[0], Element)
  assert last_result[0].tag == 'Constant'
