from pygradecode.ast_to_xml import *
import lxml 

# Grade result -------------------------------------

def test_xml():
    code = "add_two = lambda x: x + 2"
    xml_tree = xml(code)
    assert isinstance(xml_tree, lxml.etree._Element)
    

