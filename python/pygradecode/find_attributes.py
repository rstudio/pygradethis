from copy import deepcopy

from lxml.etree import _Element as Element

from .ast_to_xml import xml
from .grade_code_found import GradeCodeFound
from .find_utils import uses, flatten_list

def find_attributes(code: str | GradeCodeFound) -> GradeCodeFound:
  """Find top-level attribute access in the code.

  Attributes could be a property, a method call, or any other AST
  types where user calls <object>.<attribute>

  Unlike some other find_*() functions, this one simply grabs all
  instances without matching on anything in particular. The reason for
  this is because it is hard to specify matches for any arbitrary ASTs.
  To target specific things, use other find functions following this
  to narrow down the query.

  Parameters
  ----------
  code : str | GradeCodeFound
      a string for the source code, or a GradeCodeFound for chaining queries

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
  request = ''
  result = []

  attrs = xml_tree.xpath(".//Attribute")

  if len(attrs) > 0:
    result.extend(
      flatten_list(
        a.xpath("../..") # go up to the grandparent node (to go above <value> or <func>)
        for a in attrs
      )
    )

  return gcf.push(request_type=request_type, request=request, result=result)

def find_properties(code: str | GradeCodeFound, match: str = "") -> list[Element]:
  """Find property access in the code.

  For example, one could access a field like `df.shape`

  Parameters
  ----------
  code : str | GradeCodeFound
      a string for the source code, or a GradeCodeFound for chaining queries
  match : str, optional
      a particular property, by default None

  Returns
  -------
  list[Element]
      either a list of Element(s) or empty list if no Attribute was found
  """
  if not isinstance(code, str) and not isinstance(code, GradeCodeFound):
    raise Exception("`code` should be a `str` or `GradeCodeFound`")
  
  gcf = deepcopy(code) if isinstance(code, GradeCodeFound) else GradeCodeFound(code)
  xml_tree = xml(gcf.source) if isinstance(code, GradeCodeFound) else xml(code)

  request_type = 'property'
  request = match
  result = []

  if match == "":
    xpath_query = ".//Expr/*/Attribute/../.." 
  else:
    xpath_query = f".//attr[text()='{match}']/ancestor::Expr"
  
  props = xml_tree.xpath(xpath_query)
  result.extend(props)

  return gcf.push(request_type=request_type, request=request, result=result)

# TODO: implement find_method_chains()
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
