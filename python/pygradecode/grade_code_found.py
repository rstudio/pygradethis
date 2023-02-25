
from copy import copy
from typing import Tuple, Optional

from .xml_utils import get_node_source
from lxml.etree import _Element as Element

class GradeCodeFound:
  code: str
  # types hold the types of requests (e.g. 'function' for find_functions())
  types: list[str]
  # requests hold the specific requests (e.g. 'sum' for find_functions())
  requests: list[str]
  # results hold the list of XML element results for each request
  results: list[list[Element]]

  def __init__(self, code: str = "") -> None:
    self.code = code
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
    return [get_node_source(self.code, node=tree) for tree in last_result]

  def __repr__(self):
    last_state = self.get_last_state()

    if last_state is not None:
      last_type = last_state[0]
      last_request = last_state[1]
      last_result = last_state[2]
    else:
      return "No request has been made yet on the code"

    # code
    intro_str = f"── pygradecode found ──\n{self.code.strip()}\n"

    # type of request and specific request (if any)
    request_str = f"── Request ──\n{last_type} {last_request}"
    num_results_str = (
      f"Found {len(last_result)} {'result' if len(last_result) == 1 else 'results'}.\n"
    )

    # result
    output = [intro_str, request_str, num_results_str]
    for i, element_source in enumerate(self.get_result_source(last_result)):
      # TODO we need to better handle unicode escaping, this is buggy currently
      output.append(f"── Result {i + 1} ──\n{element_source.decode('raw_unicode_escape')}\n")
    return "\n".join(output)
