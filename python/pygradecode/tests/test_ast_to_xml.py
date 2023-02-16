from pygradecode.ast_to_xml import xml
from lxml.etree import _Element as Element

def test_xml():
  code = "add_two = lambda x: x + 2"
  xml_tree = xml(code)
  assert isinstance(xml_tree, Element)

