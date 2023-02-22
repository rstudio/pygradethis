from .xml_utils import get_node_source

from typing import Optional
from lxml.etree import _Element as Element

class GradeCodeFound:
  code: str
  # types hold the types of requests (e.g. 'function' for find_functions())
  types: list[str]
  # requests hold the specifici requests (e.g. 'sum' for find_functions())
  requests: list[str]
  # results hold the list of XML element results for each request
  results: list[Element]

  def __init__(self, code: str = "") -> None:
    self.code = code
    self.types = []
    self.requests = []
    self.results = []

  def push(self, request_type: str, request: str, result: str):
    self.types.append(request_type)
    self.requests.append(request)
    self.results.append(result)
    return self
  
  def get_last_result(self):
    return (
      self.types[-1],
      self.requests[-1],
      self.results[-1]
    )

  def get_result_source(self, last_result):
    return [get_node_source(self.code, node=tree) for tree in last_result]

  # TODO if we implement an extract_elements() that would clean up this method
  def __repr__(self):
    last_state = self.get_last_result()
    last_type = last_state[0]
    last_request = last_state[1]
    last_result = last_state[2]

    # code
    print(f"── pygradecode found ──\n{self.code.strip()}\n")

    # type of request and specific request (if any)
    print(f"── Request ──\n{last_type} {last_request}")
    print(
      f"Found {len(last_result)} {'result' if len(last_result) == 1 else 'results'}.\n"
    )

    # result
    output = []
    for i, element_source in enumerate(self.get_result_source(last_result)):
      output.append(f"── Result {i + 1} ──\n{element_source}\n")
    return "\n".join(output)
