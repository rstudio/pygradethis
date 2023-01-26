from typing import Union

from .ast_to_xml import xml, Element
from .xml_classes import FoundElements

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
    return FoundElements("", [])

  xml_tree = xml(code)
  xpath = "//FunctionDef"
  if match is not None:
    xpath = f"//FunctionDef[name='{match}']"
  
  query_result = xml_tree.xpath(xpath)
  
  return FoundElements(code, query_result)

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
    return FoundElements("", [])

  xml_tree = xml(code)
  query_result = xml_tree.xpath("//Lambda")

  return FoundElements(code, query_result)
