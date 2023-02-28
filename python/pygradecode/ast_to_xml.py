from dataclasses import dataclass
import ast
from typing import Optional, Dict, Any

from lxml import etree as ET
from lxml.etree import _Element as Element
from lxml.etree import Element as element
from lxml.etree import SubElement

ATTRS = ("lineno", "col_offset", "end_lineno", "end_col_offset")

def ast_node_attrs(ast_node: ast.AST) -> Dict[str, Any]:
  """Given an AST node, return all of its attributes

  Parameters
  ----------
  ast_node : ast.AST
      The AST node

  Returns
  -------
  Dict
      A dictionary for the attribute name : value
  """
  attrs = {}
  for key in ATTRS:
    try:
      attrs[key] = str(getattr(ast_node, key))
    except AttributeError:
      continue
  return attrs

def visit_node(
  ast_node: ast.AST,
  parent_xml_node: Optional[Element] = None,
  parser: ET.XMLParser = ET.XMLParser(remove_blank_text=True)
) -> Element:
  """Given an AST node, traverse the tree while creating an XML Element tree.

  Parameters
  ----------
  ast_node : ast.AST
      The root node
  parent_xml_node : Optional[Element], optional
      The parent node, by default None

  Returns
  -------
  Element
      The root Element
  """
  xml_node_name = ast_node.__class__.__name__

  if parent_xml_node is None:
    xml_node = parser.makeelement(xml_node_name)
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

def xml(code: str) -> Element:
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
  ast_tree = ast.parse(code)
  return visit_node(ast_tree)

@dataclass
class literal:
  code: str

def xml_strip_location(node):
  all_nodes = [node]
  all_nodes.extend(list(node.iterdescendants()))
  for n in all_nodes:
    if n.attrib:
      n.set('lineno', '')
      n.set('end_lineno', '')
      n.set('col_offset', '')
      n.set('end_col_offset', '')
    
  return node

def expr_xml_element(code) -> str:

  if not isinstance(code, str) and code == '':
    raise Exception(f"`expr_xml()` requires a valid Python expression string")

  code = code.replace(" ", "")

  try:
    xml_tree = xml(ast.parse(code))
  except SyntaxError:
    raise Exception(f"`expr_xml()` requires a valid Python expression string")
  
  expression =  xml_tree.xpath(".//*")

  if len(expression) > 0:
    node = xml_strip_location(expression)

    return node
       
  return None

def expr_xml(code) -> str:

  if not isinstance(code, str) and code == '':
    raise Exception(f"`expr_xml()` requires a valid Python expression string")

  code = code.replace(" ", "")

  try:
    xml_tree = xml(ast.parse(code))
  except SyntaxError:
    raise Exception(f"`expr_xml()` requires a valid Python expression string")
  
  expression =  xml_tree.xpath("//Expr/value/*[1]")

  if len(expression) > 0:
    node = xml_strip_location(expression.pop())

    return ET.tostring(node).decode()
       
  return code