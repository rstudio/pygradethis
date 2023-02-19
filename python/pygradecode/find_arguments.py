import itertools
from lxml.etree import _Element as Element

from .ast_to_xml import xml
from .find_functions import get_call_from_id
from .xml_classes import GradeCodeFound

def find_arguments(code: str, match: str = "") -> GradeCodeFound:
  """Find arguments of function calls in the code.

  Parameters
  ----------
  code : str
      the source code
  match : str, optional
      a particular function name, by default None

  Returns
  -------
  list[Element]
      list of XML elements corresponding to function definitions
  
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
