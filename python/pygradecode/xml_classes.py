from dataclasses import dataclass
from .ast_to_xml import Element, get_source

@dataclass
class FoundElements:
  src: str
  elements: list[Element]

  def __repr__(self):
    print(f"── pygradecode found ──\n{self.src}\n")

    if len(self.elements) == 1:
      return f"Found 1 result\n\n── Result 1 ──\n{get_source(self.src, target_node=self.elements[0])}\n"

    output = []
    for i, tree in enumerate(self.elements):
      output.append(f"── Result {i + 1} ──\n{get_source(self.src, target_node=tree)}\n")
    return "\n".join(output)

