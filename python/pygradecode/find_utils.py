from lxml.etree import _Element as Element

def get_ancestor_node(node: Element) -> Element:
  ancestor = None
  for n in node.iterancestors():
    if hasattr(n, "attrib") and len(n.attrib) > 0:
      ancestor = n
      break

  return ancestor

# general `uses()` function to check if `find_*()` finds results based on queries
def uses(function, *args, **kwargs):
  return len(function(*args, **kwargs).elements) > 0