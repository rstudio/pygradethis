import itertools
from dataclasses import dataclass
from typing import Union, Optional, AnyStr

from lxml.etree import _Element as Element

from .ast_to_xml import xml
from .find_functions import get_call_from_id
from .find_utils import uses
from .xml_utils import get_node_source
from .xml_classes import GradeCodeFound

@dataclass
class Arg:
  """A dataclass to represent a function's argument or keyword argument"""
  name: Optional[str] = ''
  value: AnyStr = None

@dataclass
class ArgList:
  """A dataclass to represent a function's argument or keyword argument"""
  args: Optional[Arg] = None

def arg(*args: AnyStr, **kwargs: AnyStr) -> ArgList:
  """Returns a list of Arg objects for positional (unnamed) argument values 
  or keyword arguments to facilitate finding arguments in function calls.

  Returns
  -------
  Union[Arg, list[Arg]]
      an Arg object that holds the name (if named argument) and value OR
      a list of Arg objects if there's several keyword arguments
  """
  all_args = []

  # first add the positional arguments
  if len(args) > 0:
    positional = list(args)
    all_args.extend([Arg(value = arg) for arg in positional])

  # then, add the keyword arguments
  if len(kwargs) != 0:
    all_kwargs = list(kwargs.items())
    # this is extracting the name = value
    all_args.extend(Arg(kwarg[0], f"r'{kwarg[1]}'") for kwarg in all_kwargs)

  return ArgList(all_args)

def find_arguments(code: str, match: ArgList = ArgList()) -> GradeCodeFound:
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
    raise Exception(f"{code} needs to be a str object.")
  
  if not isinstance(match, ArgList):
    raise Exception(f"{match} needs to be an Arg object.")

  xml_tree = xml(code.encode('unicode_escape'))
  query_result: list[Element] = []

  # TODO use the arg() now for the logic
  match_args = match.args
  print(match_args)

  # if there are no arguments to look for in particular, look for
  # all of the arguments in code
  if match_args is None:
    print("YO")
    query_result = [
      x_tree.xpath("./args/*|./keywords/*")
      for x_tree in xml_tree.xpath("//Call")
    ]
    query_result = list(itertools.chain(*query_result))
    print(query_result)
  else:
    # Extracting each keyword pair is a bit tricky because a value
    # could be any ast node so there is no way to have one query
    # satisfy all types of nodes. So, instead we look at the
    # <keyword> and its <value> node source text
    kwarg_values = [v for v in xml_tree.xpath("//keyword/value/*")]
    kwargs_pairs = [
      get_node_source(code, kw).decode('unicode_escape') 
      for kw in kwarg_values
    ]
    split_value_strings = [p.split("=") for p in kwargs_pairs]

    # construct Arg()s so we can match specified ones
    source_args = [
      Arg(name=s[0].strip(), value='='.join(s[1:]).strip()) 
      for s in split_value_strings
    ]

    if all(ma in source_args for ma in match_args):
      query_result.extend(kwarg_values)

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
