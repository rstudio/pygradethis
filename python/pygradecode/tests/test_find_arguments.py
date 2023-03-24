from lxml.etree import _Element as Element

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
  assert all(isinstance(e, Arg) for e in last_result)
  assert last_result[0].xml_node.tag == 'Constant'

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
  assert isinstance(last_result[0], Arg)
  assert last_result[0].xml_node.tag == 'List'
  assert isinstance(last_result[0].xml_node, Element)

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
  assert isinstance(last_result[0], KWArg)
  assert last_result[0].keyword_xml_node.tag == 'keyword'
  assert isinstance(last_result[0].keyword_xml_node, Element)

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
  assert isinstance(last_result[0], KWArg)
  assert last_result[0].keyword_xml_node.tag == 'keyword'
  assert isinstance(last_result[0].keyword_xml_node, Element)
