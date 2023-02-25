import itertools
from dataclasses import dataclass
from typing import Union, Optional, AnyStr

from lxml.etree import _Element as Element

from .ast_to_xml import xml
from .xml_utils import get_node_source
from .find_functions import get_call_from_id
from .find_utils import uses
from .grade_code_found import GradeCodeFound

@dataclass
class Arg:
  """A dataclass to represent a function's argument or keyword argument"""
  name: Optional[str] = ''
  value: AnyStr = None

@dataclass
class ArgList:
  """A dataclass to represent a function's argument or keyword argument"""
  args: Optional[Arg] = None

def args(*args: AnyStr, **kwargs: AnyStr) -> ArgList:
  """Returns a list of Arg objects for positional (unnamed) argument values 
  or keyword arguments to facilitate finding arguments in function calls.

  Returns
  -------
  ArgList
      an ArgList object that holds a list of Arg(s)
  """
  all_args = []

  # first add the positional arguments
  if len(args) > 0:
    positional = list(args)
    all_args.extend([
      # because Python eagerly evaluates all arguments passed in to args()
      # we have to specially handle the quoting of them: 
      # - if the argument was meant to be a `str` we double quote `"` it
      # - anything else we just wrap into a normal string
      Arg(value = f'"{arg}"' if isinstance(arg, str) else f'{arg}')
      for arg in positional
    ])

  # then, add the keyword arguments
  if len(kwargs) != 0:
    all_kwargs = list(kwargs.items())
    # this is extracting the name = value
    all_args.extend(
      # similar logic to positional arguments here, where kwargs value strings
      # are quoted if it's meant to be a `str`
      Arg(kwarg[0], f'"{kwarg[1]}"' if isinstance(kwarg[1], str) else f'{kwarg[1]}') 
      for kwarg in all_kwargs
    )

  return ArgList(all_args)

def find_arguments(
  code: str | GradeCodeFound,
  match: ArgList = ArgList()
) -> GradeCodeFound:
  """Find arguments of function calls in the code.

  Parameters
  ----------
  code : str | GradeCodeFound
      a string for the source code, or a GradeCodeFound for chaining queries
  match : ArgList
      an ArgList representing the arguments to match against

  Returns
  -------
  GradeCodeFound
      a GradeCoundFound object that holds the list of previous results
      and the current query results if any
  
  Examples
  --------
  >>> code = "sum([1, round(2.5), 3])\nprint('Hello', 'World!', sep=', ')"
  >>> find_arguments(code)
  ── pygradecode found ──
  print(1, "2", sep=", ", end=foo(x = ["\n"]))

  ── Request ──
  arguments 
  Found 5 results.

  ── Result 1 ──
  1

  ── Result 2 ──
  "2"

  ── Result 3 ──
  sep=", "

  ── Result 4 ──
  end=foo(x = ["\n"]))

  ── Result 5 ──
  x = ["\n"])
  """
  if not isinstance(code, str) and not isinstance(code, GradeCodeFound):
    raise Exception("`code` should be a `str` or `GradeCodeFound`")
  
  gcf = code if isinstance(code, GradeCodeFound) else GradeCodeFound(code)
  xml_tree = xml(gcf.code) if isinstance(code, GradeCodeFound) else xml(code)

  request_type = 'arguments'
  # TODO create a __str__ representation for ArgList
  request = ''
  results = []

  # Note: we have to encode the code to escape it properly
  xml_tree = xml(code.encode('unicode_escape'))
  match_args = match.args

  # if there are no arguments to look for in particular, look for
  # all of the arguments in code
  if match_args is None:
    results = [
      x_tree.xpath("./args/*|./keywords/*")
      for x_tree in xml_tree.xpath("//Call")
    ]
    results = list(itertools.chain(*results))
  else:
    # Extracting each keyword pair is a bit tricky because a value
    # could be any ast node so there is no way to have one query
    # satisfy all types of nodes. So, instead we look at the
    # <keyword> and its <value> node source text to reconstruct them.
    
    # extract the positional args
    positional_arg_values = [get_node_source(code, x).decode('unicode_escape') for x in xml_tree.xpath("//args/*")]
    positional_arg_values

    # construct Arg() for positional arguments
    code_args_list = [Arg("", f"{v}") for v in positional_arg_values]
    code_args_list

    # extract the keyword args
    kwarg_names = [x.text for x in xml_tree.xpath("//keyword/arg")]
    kwarg_values = [v for v in xml_tree.xpath("//keyword/value/*")]

    # get the textual form for them
    kwargs_values_strings = [get_node_source(code, kw).decode('unicode_escape') for kw in kwarg_values]
    # combine them into pairs
    kwargs_pairs = list(zip(kwarg_names, kwargs_values_strings))
    # construct the list of Arg(s) from the keyword pairs
    code_kwargs_list = [Arg(k, v) for k, v in kwargs_pairs]

    # combine the args with the kwargs
    all_code_args = code_args_list + code_kwargs_list

    # check that each argument we are trying to match against exists in the 
    # code arguments
    results = []
    for m in match_args:
      if m in all_code_args:
        results.append(m)

  # TODO make the chaining work well
  return gcf.push(request_type=request_type, request=request, results=results)

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
