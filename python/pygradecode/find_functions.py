from typing import Union

from lxml.etree import Element
from .ast_to_xml import xml
from .xml_classes import GradeCodeFound

def find_functions(code: str, match: str = None) -> Union[Element, None]:
  """Find function calls within code.

  Parameters
  ----------
  code : str
      the source code
  match : str, optional
      a particular function name, by default None

  Returns
  -------
  list[Element]
      list of XML elements corresponding to function definitions
  
  Examples
  --------
  >>> source = 'sum([1,2,3])\nsum([1,2,3])\nlen([1,2,3])'
  >>> find_functions(source)
  ── pygradecode found ──
  sum([1,2])
  sum([1,2,3])
  len([1,2,3])

  ── Result 1 ──
  sum([1,2])

  ── Result 2 ──
  sum([1,2,3])

  ── Result 3 ──
  len([1,2,3])
  >>> find_functions(source, "sum")
  ── pygradecode found ──
  sum([1,2])
  sum([1,2,3])
  len([1,2,3])

  ── Result 1 ──
  sum([1,2])

  ── Result 2 ──
  sum([1,2,3])
  """
  if not isinstance(code, str):
    return GradeCodeFound("", [])

  xml_tree = xml(code)
  xpath = "//Call/func/Name"
  
  if match is not None:
    xpath = f'//Call//func/Name/id[.="{match}"]'
    query_result = xml_tree.xpath(xpath)
    if len(query_result) > 0:
      # grab the parent of the id element in order to view the source text
      # since id is not an ast.AST
      query_result = [r.getparent() for r in query_result]
  else:
    query_result = xml_tree.xpath(xpath)

  return GradeCodeFound(code, query_result)

def uses_function(code: str, match: str = None) -> bool:
  """Check if the code uses functions.

  Parameters
  ----------
  code : str
      the source code
  match : str, optional
      function name(s), by default None

  Returns
  -------
  bool
      True if found, False otherwise

  Examples
  --------
  >>> uses_function(source, "round")
  False
  """
  found = find_functions(code, match)
  return len(found.elements) > 0

def find_function_defs(code: str, match: str = None) -> Union[Element, None]:
  """Find function definitions within code.

  Parameters
  ----------
  code : str
      the source code
  match : str, optional
      a particular function definition name, by default None

  Returns
  -------
  list[Element]
      list of XML elements corresponding to function definitions
  
  Examples
  --------
  >>> source = '\ndef foo():\n  return "foo"\n\ndef bar():\n  return "bar"\n'
  >>> find_function_defs(source)
  ── pygradecode found ──

  def foo():
    return "foo"

  def bar():
    return "bar"


  ── Result 1 ──
  def foo():
    return "foo"

  ── Result 2 ──
  def bar():
    return "bar"
  """
  if not isinstance(code, str):
    return GradeCodeFound("", [])

  xml_tree = xml(code)
  xpath = "//FunctionDef"
  if match is not None:
    xpath = f"//FunctionDef[name='{match}']"
  
  query_result = xml_tree.xpath(xpath)

  return GradeCodeFound(code, query_result)

def find_lambdas(code: str) -> list[Element]:
  """Find lambdas within code.

  Parameters
  ----------
  code : str
      the source code

  Returns
  -------
  list[Element]
      list of XML elements corresponding to lambdas

  Examples
  --------
  >>> source = "add_two = lambda x: x + 1\nadd_two(1)"
  >>> find_lambdas(source)
  ── pygradecode found ──

  add_two = lambda x: x + 2
  add_two(1)


  Found 1 result

  ── Result 1 ──
  add_two = lambda x: x + 2
  """
  if not isinstance(code, str):
    return GradeCodeFound("", [])

  xml_tree = xml(code)
  query_result = xml_tree.xpath("//Lambda")

  return GradeCodeFound(code, query_result)
