from copy import deepcopy

from lxml.etree import _Element as Element

from .ast_to_xml import xml
from .grade_code_found import GradeCodeFound
from .find_utils import uses, flatten_list

def find_methods(code: str | GradeCodeFound, match: str = "") -> GradeCodeFound:
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

  if match == "":
    attrs = get_attributes(xml_tree)
    result.extend(
      flatten_list(
        a.xpath("../..") # go up to the grandparent node (parent would just be <value>)
        for a in attrs
      )
    )
  else:
    # TODO: implement logic of finding specific method calls
    ...

  return gcf.push(request_type=request_type, request=request, result=result)

def get_method_chains(code: str) -> list[Element]:
  """Get method chains in the code.

  Note: This function will return the top-level chains, so it will not
  return chains that are inside other expressions.

  Parameters
  ----------
  node : Element
      root node

  Returns
  -------
  list[Element]
      either a list of Element(s) or empty list if no Attribute was found
  """
  xml_tree = xml(code)

  return [
    a
    # if an Attribute is followed by another Attribute, we have a chain
    for a in xml_tree.xpath(".//Attribute") if a.xpath("(.//Attribute)[1]")
  ]

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
