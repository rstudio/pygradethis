import ast
from typing import Optional

from lxml.etree import _Element as Element
from lxml.etree import Element as element
from lxml.etree import SubElement

ATTRS = ("lineno", "col_offset", "end_lineno", "end_col_offset")

def ast_node_attrs(ast_node: ast.AST):
  attrs = {}
  for key in ATTRS:
    try:
      attrs[key] = str(getattr(ast_node, key))
    except AttributeError:
      continue
  return attrs

def visit_node(ast_node: ast.AST, parent_xml_node: Optional[Element] = None) -> Element:
  xml_node_name = ast_node.__class__.__name__

  if parent_xml_node is None:
    xml_node = element(xml_node_name)
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
      # for non-AST nodes, just set `type` and `text` value (content of tag)
      node = SubElement(xml_node, key)
      node.attrib["type"] = type(value).__name__
      node.text = str(value)

  return xml_node

def xml(src: str) -> Element:
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
