import itertools
from lxml.etree import _Element as Element

from .ast_to_xml import xml
from .find_functions import get_call_from_id
from .find_utils import uses
from .xml_classes import GradeCodeFound

def find_arguments(code: str, match: str = "") -> GradeCodeFound:
  """Find arguments of function calls in the code.

  Parameters
  ----------
  code : str
      the source code
  match : str, optional
      a particular argument name, by default None

  Returns
  -------
  list[Element]
      list of XML elements corresponding to function arguments
  
  Examples
  --------
  >>> code = "sum([1, round(2.5), 3])\nprint('Hello', 'World!', sep=', ')"
  >>> find_arguments(code)
  ── pygradecode found ──
  sum([1, round(2.5), 3])
  print('Hello', 'World!', sep=', ')

  ── Result 1 ──
  [1, round(2.5), 3]

  ── Result 2 ──
  2.5

  ── Result 3 ──
  'Hello'

  ── Result 4 ──
  'World!'

  ── Result 5 ──
  sep=', '
  >>> find_arguments(code, 'sum')
  ── pygradecode found ──
  sum([1, round(2.5), 3])
  print('Hello', 'World!', sep=', ')

  Found 1 result

  ── Result 1 ──
  [1, round(2.5), 3]
  >>> find_arguments(code, 'round')
  ── pygradecode found ──
  sum([1, round(2.5), 3])
  print('Hello', 'World!', sep=', ')

  Found 1 result

  ── Result 1 ──
  2.5
  """
  if not isinstance(code, str):
    return GradeCodeFound()

  xml_tree = xml(code)
  query_result: list[Element] = []

  # TODO instead of matching on a function, we should be matching on an argument name
  # OR
  # TODO If `match` is an empty string, find unnamed arguments

  if match != "":
    # we have to drill down to <id> node to check if a particular function name exists
    xpath = f'//Call//func/Name/id[.="{match}"]'
    id_nodes = xml_tree.xpath(xpath)

    if len(id_nodes) > 0:
      # first get the call node for each of these specific <id> nodes
      call_nodes = [get_call_from_id(n) for n in id_nodes]

      # for every Call node, we want to combine the args / keywords because
      # these are 2 separate nodes in Python
      query_result = [
        x_tree.xpath("./args/*|./keywords/*")
        for x_tree in call_nodes
      ]
      query_result = list(itertools.chain(*query_result))
  else:
    query_result = [
      x_tree.xpath("./args/*|./keywords/*")
      for x_tree in xml_tree.xpath("//Call")
    ]
    query_result = list(itertools.chain(*query_result))

  return GradeCodeFound(code, query_result)

def uses_argument(code: str, match: str = "") -> bool:
  """Check if the code has arguments.

  Parameters
  ----------
  code : str
      the source code
  match : str, optional
      argument name(s), by default None

  Returns
  -------
  bool
      True if found, False otherwise

  Examples
  --------
  >>> code = "print('Hello', 'World!', sep=', ')"
  >>> uses_argument(code, "sum")
  True
  >>> uses_argument(code, "round")
  False
  """
  return uses(find_arguments, code, match)
