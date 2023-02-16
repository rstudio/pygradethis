from typing import Union

from lxml.etree import _Element as Element
from .ast_to_xml import xml
from .xml_classes import GradeCodeFound
from .find_utils import uses

def find_functions(code: str, match: str = None) -> Union[Element, None]:
  """Find function calls in the code.

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
  >>> code = 'sum([1,2,3])\nsum([1,2,3])\nlen([1,2,3])'
  >>> find_functions(code)
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
  >>> find_functions(code, "sum")
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
    return GradeCodeFound()

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
  >>> code = 'sum([1,2,3])'
  >>> uses_function(code, "sum")
  True
  >>> uses_function(code, "round")
  False
  """
  return uses(find_functions, code, match)

def find_lambdas(code: str) -> list[Element]:
  """Check if there are lambdas in the code.

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
  >>> code = "add_two = lambda x: x + 1\nadd_two(1)"
  >>> find_lambdas(code)
  ── pygradecode found ──

  add_two = lambda x: x + 2
  add_two(1)


  Found 1 result

  ── Result 1 ──
  add_two = lambda x: x + 2
  """
  if not isinstance(code, str):
    return GradeCodeFound()

  xml_tree = xml(code)
  query_result = xml_tree.xpath("//Lambda")

  return GradeCodeFound(code, query_result)

def uses_lambda(code: str) -> bool:
  """Find lambdas within code.

  Parameters
  ----------
  code : str
      the source code

  Returns
  -------
  bool
      True if found, False otherwise

  Examples
  --------
  >>> code = 'add_two = lambda x: x + 2'
  >>> uses_lambda(code)
  True
  >>> code = 'def add_two():\n  return x + 2'
  >>> uses_lambda(code)
  False
  """
  return uses(find_lambdas, code)
