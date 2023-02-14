from lxml import etree
from lxml.etree import Element

### XML Print methods

def prettify(xml_tree: Element) -> None:
  # Note: tostring() returns bytes, so we decode() it
  print(etree.tostring(xml_tree, pretty_print=True).decode())
