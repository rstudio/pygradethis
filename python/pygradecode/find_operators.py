from .ast_to_xml import xml
from .find_utils import uses
from .grade_code_found import GradeCodeFound

# operator symbol to ast node name
OPERATORS = {
  # unary ops
  '~': 'Invert', 'not': 'Not',
  # infix operators
  'and': 'And', 'or': 'Or',
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
  # cmp ops
  '==': 'Eq', '!=': 'NotEq', '<': 'Lt', '<=': 'LtE', '>': 'Gt', '>=': 'GtE',
  'is': 'Is', 'is not': 'IsNot', 'in': 'In', 'not in': 'NotIn'
}

# unaryops
# NOTE: we separate these because +/- are unary operators that
# could get confused for the Add/Sub
UNARY_OPS = {'+': 'UAdd', '-': 'USub'}

def get_operator(op: str) -> list[str]:
  # check if op is valid
  if op not in OPERATORS and op not in UNARY_OPS:
    raise Exception(f"{op} is not a valid operator in Python!")

  # we may get an overlap of operators as a Binary or Unary operator
  # so we will try to combine the valid ones in a list
  return [o for o in [OPERATORS.get(op), UNARY_OPS.get(op)] if o is not None]

def find_operators(code: str | GradeCodeFound, match: str = "") -> GradeCodeFound:
  """Find operators in the code.

  NOTE: currently, the output is not super helpful because we're
  printing the first ancestor which has the location attributes
  to return source text. In the future, this will be solved by
  incorporating `rich` to bold/underline within the original code text.

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

  ── Request ──
  operators 
  Found 4 results.

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

  ── Request ──
  operators -
  Found 1 result.

  ── Result 1 ──
  -1
  >>> find_operators(code, "//")
  ── pygradecode found ──
  -1 + 2 * 3 // 4

  ── Request ──
  operators //
  Found 1 result.

  ── Result 1 ──
  2 * 3 // 4
  """
  if not isinstance(code, str) and not isinstance(code, GradeCodeFound):
    raise Exception("`code` should be a `str` or `GradeCodeFound`")
  
  gcf = code if isinstance(code, GradeCodeFound) else GradeCodeFound(code)
  xml_tree = xml(gcf.source) if isinstance(code, GradeCodeFound) else xml(code)

  request_type = 'operators'
  request = match
  result = []
  
  if match != "":
    matched_ops = get_operator(match)
    # construct query to grab the specific matched operators
    xpath = "|".join(f"//op/{mo}" for mo in matched_ops)
    result = xml_tree.xpath(xpath)
  else:
    result = xml_tree.xpath("//op/*")

  return gcf.push(request_type=request_type, request=request, result=result)
