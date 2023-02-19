import textwrap
from typing import Union

from lxml import etree
from lxml.etree import _Element as Element

from .ast_to_xml import xml
from .find_utils import get_ancestor_node

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
  except (AttributeError, KeyError):
    # if unsuccessful, we will return the entire code itself
    pass

  return code

def get_source(
  code: str, node: Element, xpath: str = ""
) -> Union[list[str], str]:
  """Return the source code for a particular XPath query or a target XML element.

  Parameters
  ----------
  code : str
      the source code
  xpath : str, optional
      an XPath query, by default None
  node : Element, optional
      a target XML element, by default None

  Returns
  -------
  list[str] | str
      Return a list of source code if there are multiple instances for an 
      XPath query or, return a single piece of source code for a given target XML 
      element node.
  """
  xml_tree = xml(code)

  src_lines = code.splitlines()

  if node is not None:
    return get_source_lines(src_lines, node)

  if xpath != "":
    sources = []
    for node in xml_tree.xpath(xpath):
      code = get_source_lines(src_lines, node)
      sources.append(code)
    return sources
  
  return code

def get_node_source(code: str, node: Element) -> str:
  target_code = get_source_lines(code.splitlines(), node)

  try:
    node_with_location = get_ancestor_node(node)
    start_col = int(node_with_location.attrib['col_offset'])
    end_col = int(node_with_location.attrib['end_col_offset'])
  except Exception:
    return code
    
  return target_code[start_col:end_col]

### XML Print methods

def prettify(xml_tree: Element) -> None:
  # Note: tostring() returns bytes, so we decode() it
  print(etree.tostring(xml_tree, pretty_print=True).decode())