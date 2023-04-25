import ast
import textwrap
from typing import Optional, Dict, Any

from lxml import etree as ET
from lxml.etree import _Element as Element
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


# Get source text ----

def get_source_lines(
  src_lines: list[str],
  node: Element,
  dedent: bool = True
) -> str:
  code = "\n".join(src_lines)

  # attempt to extract source code lines relevant to the target node
  try:
    # extract ranges
    start_lineno = int(node.attrib["lineno"]) - 1
    end_lineno = int(node.attrib["end_lineno"])
    
    # turn the relevant lines it into one string
    code = "\n".join(src_lines[start_lineno:end_lineno])
    if dedent:
      code = textwrap.dedent(code)
  except (AttributeError, KeyError, ValueError):
    # if unsuccessful, we will return the entire code itself
    pass

  return code
