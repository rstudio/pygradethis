from dataclasses import dataclass
from lxml.etree import Element
from .ast_to_xml import get_source

@dataclass
class GradeCodeFound:
  src: str
  elements: list[Element]

  def __repr__(self):
    print(f"── pygradecode found ──\n{self.src.strip()}\n")

    # TODO: add Request in output so it's clear what type of request it is (e.g. functions)
    if len(self.elements) == 1:
      return f"Found 1 result\n\n── Result 1 ──\n{get_source(self.src, target_node=self.elements[0])}\n"

    output = []
    for i, tree in enumerate(self.elements):
      output.append(f"── Result {i + 1} ──\n{get_source(self.src, target_node=tree)}\n")
    return "\n".join(output)
