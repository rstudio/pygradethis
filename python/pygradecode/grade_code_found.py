
from copy import copy
from typing import Tuple, Optional

from lxml.etree import _Element as Element

from .ast_to_xml import xml, get_source_lines
from .find_utils import get_ancestor_node

class GradeCodeFound:
  source: str
  # types hold the types of requests (e.g. 'function' for find_functions())
  types: list[str]
  # requests hold the specific requests (e.g. 'sum' for find_functions())
  requests: list[str]
  # results hold the list of XML element results for each request
  results: list[list[Element]]

  def __init__(self, code: str = "") -> None:
    self.source = code
    self.types = []
    self.requests = []
    self.results = []

  def push(
      self, 
      request_type: str, 
      request: str, 
      results: list[Element]
    ) -> 'GradeCodeFound':
    self.types.append(request_type)
    self.requests.append(request)
    self.results.append(results)
    return copy(self)
  
  def has_previous_request(self) -> bool:
    return len(self.requests) > 0
  
  @property
  def last_result(self):
    if self.has_previous_request():
      return self.results[-1]
    else:
      return []
  
  def get_last_state(self) -> Optional[Tuple[str, str, list[Element]]]:
    if self.has_previous_request():
      return (
        self.types[-1],
        self.requests[-1],
        self.results[-1]
      )
    return None

  def get_result_source(self, last_result: list[Element]) -> list[str]:
    return [get_node_source(self.source, node=tree) for tree in last_result]

  def __repr__(self):
    last_state = self.get_last_state()

    if last_state is not None:
      last_type = last_state[0]
      last_request = last_state[1]
      last_result = last_state[2]
    else:
      return "No request has been made yet on the code"

    # code
    intro_str = f"── pygradecode found ──\n{self.source.strip()}\n"

    # type of request and specific request (if any)
    request_str = f"── Request ──\n{last_type} {last_request}"
    num_results_str = (
      f"Found {len(last_result)} {'results' if len(last_result) > 1 else 'result'}.\n"
    )

    # result
    output = [intro_str, request_str, num_results_str]
    for i, element_source in enumerate(self.get_result_source(last_result)):
      # TODO we need to better handle unicode escaping, this is buggy currently
      if isinstance(element_source, bytes):
        element_source = element_source.decode('raw_unicode_escape')

      output.append(f"── Result {i + 1} ──\n{element_source}\n")
    return "\n".join(output)


def get_source(
  code: str, node: Element, xpath: str = ""
) -> list[str] | str:
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

def get_node_source(code: str | GradeCodeFound, node: Optional[Element]) -> str:
  if node is None:
    return ''
  
  if isinstance(code, GradeCodeFound):
    code = code.source
  
  target_code = get_source_lines(code.splitlines(), node)

  try:
    node_with_location = get_ancestor_node(node)
    start_col = int(node_with_location.attrib['col_offset'])
    end_col = int(node_with_location.attrib['end_col_offset'])
  except (Exception, ValueError):
    return code
    
  return target_code[start_col:end_col].encode('raw_unicode_escape')