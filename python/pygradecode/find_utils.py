import itertools
from lxml.etree import _Element as Element

def get_ancestor_node(node: Element) -> Element:
  if hasattr(node, "attrib") and len(node.attrib) > 0:
    return node

  return get_ancestor_node(node.getparent())

# general `uses()` function to check if `find_*()` finds results based on queries
def uses(function, *args, **kwargs):
  return len(function(*args, **kwargs).elements) > 0

def flatten_list(alist: list) -> list:
  return list(itertools.chain(*alist))