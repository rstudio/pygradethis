"""Module to find attributes, method calls, properties in Python code."""

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
  GradeCodeFound
      a GradeCoundFound object that holds the list of previous results
      and the current query results if any
  """
  if not isinstance(code, str) and not isinstance(code, GradeCodeFound):
    raise Exception("`code` should be a `str` or `GradeCodeFound`")
  
  gcf = deepcopy(code) if isinstance(code, GradeCodeFound) else GradeCodeFound(code)
  xml_tree = xml(gcf.source) if isinstance(code, GradeCodeFound) else xml(code)

  request_type = 'attributes'
  request = ''
  result = []

  xpath_query = ".//Attribute"

  attrs = []
  if gcf.has_previous_request():
    for node in gcf.last_result:  
      attrs.extend(node.xpath(xpath_query))
    result.extend(attrs)
  else:
    attrs = xml_tree.xpath(xpath_query)
    result.extend(
      flatten_list(
        a.xpath("../..") # go up to the grandparent node (to go above <value> or <func>)
        for a in attrs
      )
    )

  return gcf.push(request_type=request_type, request=request, result=result)

def uses_attributes(code: str) -> bool:
  """Check if the code uses attributes.

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
  >>> code = 'df.shape'
  >>> uses_attributes(code)
  True
  >>> code = 'df.head()'
  >>> uses_attributes(code)
  True
  >>> code = 'df.loc[:,'foo']'
  >>> uses_attributes(code)
  True
  >>> code = 'sum([1, 2, 3])'
  >>> uses_properties(code)
  False
  """
  return uses(find_attributes, code)

def find_properties(code: str | GradeCodeFound, match: str = "") -> GradeCodeFound:
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
  GradeCodeFound
      a GradeCoundFound object that holds the list of previous results
      and the current query results if any
  """
  if not isinstance(code, str) and not isinstance(code, GradeCodeFound):
    raise Exception("`code` should be a `str` or `GradeCodeFound`")
  
  gcf = deepcopy(code) if isinstance(code, GradeCodeFound) else GradeCodeFound(code)
  xml_tree = xml(gcf.source) if isinstance(code, GradeCodeFound) else xml(code)

  request_type = 'property'
  request = match
  result = []

  if match == "":
    xpath_query = ".//Expr/*/Attribute" 
    # TODO we have duplication of this logic to handle previous requests if it exists
    # let's refactor it out into a function if possible
    if gcf.has_previous_request():
      for node in gcf.last_result:  
        result.extend(flatten_list(node.xpath(xpath_query)))
    else:
      result.extend(xml_tree.xpath(xpath_query))
  else:
    # TODO support a list of matches
    xpath_query = f".//Expr/*/Attribute//attr[text()='{match}']/.." 
    if gcf.has_previous_request():
      for node in gcf.last_result:  
        result.extend(flatten_list(node.xpath(xpath_query)))
    else:
      result.extend(xml_tree.xpath(xpath_query))

  return gcf.push(request_type=request_type, request=request, result=result)

def uses_properties(code: str, match: str = "") -> bool:
  """Check if the code uses properties.

  Parameters
  ----------
  code : str
      the source code
  match : str, optional
      the property name(s), by default None

  Returns
  -------
  bool
      True if found, False otherwise

  Examples
  --------
  >>> code = 'df.shape'
  >>> uses_properties(code)
  True
  >>> code = 'df.head()'
  >>> uses_properties(code)
  False
  >>> code = 'df.empty'
  >>> uses_properties(code, 'empty')
  True
  >>> uses_properties(code, 'shape')
  False
  """
  return uses(find_properties, code, match)

def find_method_chains(code: str | GradeCodeFound) -> GradeCodeFound:
  """Find method chains in the code.

  Note: This function will search for the top-level chains, so it will not
  return chains that are inside other expressions.

  Parameters
  ----------
  code : str | GradeCodeFound
      a string for the source code, or a GradeCodeFound for chaining queries

  Returns
  -------
  GradeCodeFound
      a GradeCoundFound object that holds the list of previous results
      and the current query results if any
  """
  if not isinstance(code, str) and not isinstance(code, GradeCodeFound):
    raise Exception("`code` should be a `str` or `GradeCodeFound`")
  
  gcf = deepcopy(code) if isinstance(code, GradeCodeFound) else GradeCodeFound(code)
  xml_tree = xml(gcf.source) if isinstance(code, GradeCodeFound) else xml(code)

  request_type = 'property'
  request = ''

  result = [
    a
    # if an Attribute is followed by another Attribute, we have a chain
    for a in xml_tree.xpath(".//Attribute") if a.xpath("(.//Attribute)[1]")
  ]

  return gcf.push(request_type=request_type, request=request, result=result)

def uses_method_chains(code: str) -> bool:
  """Check if the code uses method chains.

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
  >>> code = 'df.head().tail()'
  >>> uses_function(code)
  True
  >>> code = 'df.head()'
  >>> uses_function(code)
  False
  """
  return uses(find_method_chains, code)
