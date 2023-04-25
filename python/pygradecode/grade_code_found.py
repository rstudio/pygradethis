from collections import namedtuple
from typing import Optional
from lxml.etree import _Element as Element
from rich.console import Console

from .ast_to_xml import get_source_lines
from .find_utils import get_ancestor_node
from .highlight_text import format_text, pgc_print

# `type` hold the types of requests (e.g. 'function' for find_functions())
# `request` hold the specific requests (e.g. 'sum' for find_functions())
# `result` holds the list of XML element results for each request
QueryResult = namedtuple("QueryResult", ['type', 'request', 'result'])

class GradeCodeFound:
  source: str
  results: list[QueryResult]

  def __init__(self, code: str = "", results: Optional[QueryResult] = None) -> None:
    self.source = code
    self.results = results if results is not None else []

  def push(
    self, 
    request_type: str, 
    request: str, 
    result: list[Element]
  ) -> 'GradeCodeFound':
    self.results.append(
      QueryResult(type=request_type, request=request, result=result)
    )
    return self
  
  def has_previous_request(self) -> bool:
    return len(self.results) > 0
  
  @property
  def last_result(self) -> list[Element]:
    if self.has_previous_request():
      return self.results[-1].result
    else:
      return []
  
  def get_last_state(self) -> QueryResult:
    if self.has_previous_request():
      return self.results[-1]
    return None

  def __repr__(self):
    pgc_print(self)
    return ""

@pgc_print.register
def _(arg: GradeCodeFound, console: Console = Console(color_system='standard')):
  last_state = arg.get_last_state()

  if last_state is None:
    return

  last_type, last_request, last_result = last_state

  # code
  console.print(f"── pygradecode found ──\n{arg.source.strip()}\n")

  # type of request and specific request (if any)
  console.print(f"── Request ──\n{last_type} {last_request}")

  console.print(
    f"Found {len(last_result)} {'results' if len(last_result) > 1 else 'result'}.\n"
  )

  # result
  for i, element in enumerate(last_result):
    console.print(f"── Result {i + 1} ──")
    formatted = format_text(arg.source, element)
    console.print(formatted.text, end="\n\n")

def get_node_source(code: str | GradeCodeFound, node: Optional[Element]) -> str:
  if node is None:
    return ''

  if isinstance(code, GradeCodeFound):
    code = code.source

  target_code = get_source_lines(
    src_lines = code.splitlines(),
    node = node,
    dedent = False # we want to preserve the whitespace
  )

  try:
    node_with_location = get_ancestor_node(node)
    start_col = int(node_with_location.attrib['col_offset'])
    end_col = int(node_with_location.attrib['end_col_offset'])
    return target_code[start_col:end_col].encode('raw_unicode_escape').decode()
  except (Exception, ValueError):
    pass