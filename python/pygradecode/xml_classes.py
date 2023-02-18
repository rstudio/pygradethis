from .xml_utils import get_node_source

from typing import Optional
from lxml.etree import _Element as Element

class GradeCodeFound:
  code: str
  elements: list[Element]

  def __init__(self, code: str = "", elements: Optional[list[Element]] = None) -> None:
    self.code = code
    self.elements = [] if elements is None else elements

  # TODO: we might also need to create a higher level type for Element so it also has 
  # its own Element field + source code field? OR a method to extract that out
  def extract_elements(self):
    return [get_node_source(self.code, node=tree) for tree in self.elements]

  # TODO if we implement an extract_elements() that would clean up this method
  def __repr__(self):
    print(f"── pygradecode found ──\n{self.code.strip()}\n")

    # TODO: add Request in output so it's clear nature of request it is (e.g. functions)
    if len(self.elements) == 1:
      source = get_node_source(self.code, node=self.elements[0])
      return f"Found 1 result\n\n── Result 1 ──\n{source}\n"

    output = []
    for i, element_source in enumerate(self.extract_elements()):
      output.append(f"── Result {i + 1} ──\n{element_source}\n")
    return "\n".join(output)
