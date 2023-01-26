import ast
import textwrap

from typing import Union, List

from lxml import etree
from lxml.etree import Element, SubElement

ATTRS = ("lineno", "col_offset", "end_lineno", "end_col_offset")

def ast_node_attrs(ast_node):
  attrs = {}
  for key in ATTRS:
    try:
      attrs[key] = str(getattr(ast_node, key))
    except AttributeError:
      continue
  return attrs

def visit_node(ast_node: ast.AST, parent_xml_node: Element=None) -> Element:
  xml_node_name = ast_node.__class__.__name__

  if parent_xml_node is None:
    xml_node = Element(xml_node_name)
  else:
    xml_node = SubElement(parent_xml_node, xml_node_name)

  xml_node.attrib.update(ast_node_attrs(ast_node))

  for key, value in ast_node.__dict__.items():
    # skip dunders for now
    if key.startswith("_") or key in ATTRS:
      continue
    if isinstance(value, ast.AST):
      sub_node = SubElement(xml_node, key)
      visit_node(value, sub_node)
    elif isinstance(value, list):
      # sometimes nodes are in a list (e.g. Module body is a [])
      # so here we only create subelements if they are all AST nodes
      if all(isinstance(x, ast.AST) for x in value):
        sub_node = SubElement(xml_node, key)
        for node in value:
          visit_node(node, sub_node)
    else:
      # for non-AST nodes, just set `type` and `text` value
      node = SubElement(xml_node, key)
      node.attrib["type"] = type(value).__name__
      node.text = str(value)

  return xml_node

def xml(src: str) -> list[Element]:
  """Return an XML tree of Python source code representing the AST.

  Parameters
  ----------
  src : str
      source code text

  Returns
  -------
  list[Element]
      a list of Element(s)
  """
  ast_tree = ast.parse(src)
  return visit_node(ast_tree)

def get_source_lines(src_lines: list[str], node: Element, dedent=True):
  code = "\n".join(src_lines)

  # attempt to extract source code lines relevant to the target node
  try:
    # extract ranges
    start_lineno = int(node.attrib["lineno"]) - 1
    end_lineno = int(node.attrib["end_lineno"])
    
    # turn the relevant lines it into one string
    code = "\n".join( src_lines[start_lineno:end_lineno])
    if dedent:
      code = textwrap.dedent(code)
  except (AttributeError, KeyError) as error:
    # if unsuccessful, we will return the entire code itself
    pass

  return code

def get_source(code: str, xpath: str = None, target_node: Element = None) -> Union[List[str], str]:
  """Return the source code for a particular XPath query or a target XML element.

  Parameters
  ----------
  code : str
      the source code
  xpath : str, optional
      an XPath query, by default None
  target_node : Element, optional
      a target XML element, by default None

  Returns
  -------
  list[str] | str
      Return a list of source code if there are multiple instances for an XPath query or,
      return a single piece of source code for a given target XML element node
  """
  xml_tree = xml(code)

  src_lines = code.split("\n")

  if target_node is not None:
    return get_source_lines(src_lines, target_node)

  if xpath is not None:
    sources = []
    for node in xml_tree.xpath(xpath):
      code = get_source_lines(src_lines, node)
      sources.append((code, node.attrib))
    return sources
  
  return code
