from .ast_to_xml import Element, etree

### XML Print methods

def prettify(xml_tree: Element) -> None:
  # Note: tostring() returns bytes, so we decode() it
  print(etree.tostring(xml_tree, pretty_print=True).decode())
