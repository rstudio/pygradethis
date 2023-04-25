import itertools
from typing import Optional

from lxml.etree import _Element as Element

def get_ancestor_node(node: Optional[Element]) -> Optional[Element]:
  if node is None or (hasattr(node, "attrib") and len(node.attrib) > 0):
    return node

  return get_ancestor_node(node.getparent())

# general `uses()` function to check if `find_*()` finds results based on queries
def uses(function, *args, **kwargs):
  return len(function(*args, **kwargs).last_result) > 0

def flatten_list(alist: list | list[list]) -> list:
  return list(itertools.chain(*alist))