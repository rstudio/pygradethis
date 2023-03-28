from copy import deepcopy
from typing import Optional, AnyStr

from lxml.etree import _Element as Element

from .ast_to_xml import xml
from .grade_code_found import GradeCodeFound
from .find_utils import uses

def find_method_calls(code: str | GradeCodeFound, match: str = "") -> GradeCodeFound:
  """Find method calls in the code.

  Parameters
  ----------
  code : str | GradeCodeFound
      a string for the source code, or a GradeCodeFound for chaining queries
  match : str, optional
      a particular method name, by default None

  Returns
  -------
  list[Element]
      list of XML elements corresponding to method calls
  """
  if not isinstance(code, str) and not isinstance(code, GradeCodeFound):
    raise Exception("`code` should be a `str` or `GradeCodeFound`")
  
  gcf = deepcopy(code) if isinstance(code, GradeCodeFound) else GradeCodeFound(code)
  xml_tree = xml(gcf.source) if isinstance(code, GradeCodeFound) else xml(code)

  request_type = 'methods'
  request = match
  result = []

  # TODO: implement logic of finding all method calls

  return gcf.push(request_type=request_type, request=request, result=result)

def get_attributes(node: Element, attrs: list = None) -> list[Element]:
  """Given a starting root Element node, return all Attribute(s)

  Parameters
  ----------
  node : Element
      root node
  attrs : list, optional
      a list to keep track of found Attribute(s), by default None

  Returns
  -------
  list[Element]
      either a list of Element(s) or empty list if no Attribute was found
  """
  attrs = [] if attrs is None else attrs
  attr = node.xpath("(.//Attribute)[1]")

  if len(attr) == 0:
    return []
 
  attrs.extend(attr)

  get_attributes(attr[0], attrs)
  return attrs
