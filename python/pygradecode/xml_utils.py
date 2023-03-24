from copy import copy
from dataclasses import dataclass
from typing import Any

from lxml import etree as ET
from lxml.etree import _Element as Element
from lxml.doctestcompare import LXMLOutputChecker

from .ast_to_xml import xml

# low-level functions ----

@dataclass
class literal:
  source: str

  def __init__(self, source) -> None:
    if not isinstance(source, str):
      raise ValueError(f"`source` should be a `str`")
    self.source = source

def strip_node_location(n: Element) -> str:
  if n.attrib:
    n.set('lineno', '')
    n.set('end_lineno', '')
    n.set('col_offset', '')
    n.set('end_col_offset', '')
  return n

def xml_strip_location(node: Element) -> Element:
  """Strip the location information from an XML Element and all of its descendants.

  Parameters
  ----------
  node : Element
      the XML Element node

  Returns
  -------
  Element
      the same XML Element node with location information set to ""

  Raises
  ------
  Exception
      when a `None` is passed in for `node`
  """
  if node is None:
    raise Exception("cannot strip locations of a `None` Element")
  
  # strip the location information
  strip_node_location(node)
  
  for n in node.iterdescendants():
    strip_node_location(n)
    
  return node

def expr_xml_node(code: str) -> Element:
  if not isinstance(code, str) and code == '':
    raise Exception(f"`code` is not a valid Python expression string")

  if isinstance(code, literal):
    code = f"'{code.source}'"
  else:
    code = code.replace(" ", "").encode('raw_unicode_escape').decode()

  try:
    xml_tree = xml(code)
  except SyntaxError:
    raise Exception(f"`code` requires a valid Python expression string")
  
  nodes = xml_tree.xpath('.//Expr/value/*[1]')
  
  return nodes.pop() if len(nodes) > 0 else None

def compare_xml_nodes(n1: Any, n2: Any):
  if n1 is None or n2 is None:
    return False
  
  # use the builtin LXMLOutputChecker
  # Note: we could in the future make an `xml_checker` param
  # to swap in any checker that has a `.compare_docs()` method
  xml_checker = LXMLOutputChecker()

  try:
    # strip locations on both and compare the two elements/docs
    n1 = copy(n1)
    n2 = copy(n2)

    result = xml_checker.compare_docs(
      xml_strip_location(n1),
      xml_strip_location(n2)
    )
    return result
  except Exception:
    pass
  
  return False

# XML Print methods ----

def prettify(xml_tree: Element) -> None:
  # Note: tostring() returns bytes, so we decode() it
  print(ET.tostring(xml_tree, pretty_print=True).decode())