from lxml.etree import _Element as Element

from .ast_to_xml import xml
from .find_utils import uses
from .xml_classes import GradeCodeFound

# operator symbol to ast node name
OPERATORS = {
  # boolops
  'and': 'And', 'or': 'Or',
  # operators
  '+': 'Add',
  '-': 'Sub',
  '*': 'Mult',
  '@': 'MatMult',
  '/': 'Div',
  '%': 'Mod',
  '**': 'Pow',
  '<<': 'LShift',
  '>>': 'RShift',
  '|': 'BitOr',
  '^': 'BitXor',
  '&': 'BitAnd',
  '//': 'FloorDiv',
  # cmpops
  '==': 'Eq', '!=': 'NotEq', '<': 'Lt', '<=': 'LtE', '>': 'Gt', '>=': 'GtE',
  'is': 'Is', 'is not': 'IsNot', 'in': 'In', 'not in': 'NotIn'
}

# unaryops
# NOTE: we separate these because +/- are unary operators that
# could get confused for the Add/Sub
UNARY_OPS = {'~': 'Invert', 'not': 'Not', '+': 'UAdd', '-': 'USub'}

def get_operator(op: str) -> str:
  # check if op is valid
  if op not in OPERATORS and op not in UNARY_OPS:
    raise Exception(f"{op} is not a valid operator in Python!")

  # we may get an overlap of operators as a Binary or Unary operator
  # so we will try to combine the valid ones in a list
  return [o for o in [OPERATORS.get(op), UNARY_OPS.get(op)] if o is not None]

def find_operators(code: str, match: str = "") -> GradeCodeFound:
  """Find operators in the code.

  Parameters
  ----------
  code : str
      the source code
  match : str, optional
      a particular operator name, by default None

  Returns
  -------
  list[Element]
      list of XML elements corresponding to operators
  
  Examples
  --------
  >>> code = "-1 + 2 * 3 // 4"
  >>> find_operators(code)
  ── pygradecode found ──
  -1 + 2 * 3 // 4

  ── Result 1 ──
  -1

  ── Result 2 ──
  -1 + 2 * 3 // 4

  ── Result 3 ──
  2 * 3

  ── Result 4 ──
  2 * 3 // 4
  >>> find_operators(code, "-")
  ── pygradecode found ──
  -1 + 2 * 3 // 4

  Found 1 result

  ── Result 1 ──
  -1
  >>> find_operators(code, "//")
  ── pygradecode found ──
  -1 + 2 * 3 // 4

  Found 1 result

  ── Result 1 ──
  2 * 3 // 4
  """
  if not isinstance(code, str):
    return GradeCodeFound()

  xml_tree = xml(code)
  query_result: list[Element] = []
  
  if match != "":
    matched_ops = get_operator(match)
    # construct query to grab the specific matched operators
    xpath = "|".join(f"//op/{mo}" for mo in matched_ops)
    query_result = xml_tree.xpath(xpath)
  else:
    query_result = xml_tree.xpath("//op/*")

  return GradeCodeFound(code, query_result)
