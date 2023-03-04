import itertools
from copy import copy
from dataclasses import dataclass
from typing import Optional, AnyStr

from lxml.etree import _Element as Element

from .find_utils import uses, flatten_list
from .grade_code_found import GradeCodeFound, get_node_source
from .ast_to_xml import xml
from .xml_utils import (
  compare_xml_nodes, literal, expr_xml_node
)

@dataclass
class Arg:
  """A dataclass to represent a function's positional argument"""
  name: Optional[str] = ''
  code: AnyStr = None
  xml_node: AnyStr = None

@dataclass
class KWArg:
  """A dataclass to represent a function's keyword argument"""
  name: Optional[str] = ''
  code: AnyStr = None
  value_xml_node: AnyStr = None
  # this field is so we can refer to originating keyword XML Element
  # when it comes to match and store keyword arguments for `find_arguments()`
  keyword_xml_node: AnyStr = None

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
      Arg(
        code = arg.source if isinstance(arg, literal) else arg,
        xml_node = expr_xml_node(arg)
      )
      for arg in positional
    ])

  # then, add the keyword arguments
  if len(kwargs) != 0:
    all_kwargs = list(kwargs.items())
    # this is extracting the name = value
    all_args.extend(
      # similar logic to positional arguments here, where kwargs value strings
      # are quoted if it's meant to be a `str`
      KWArg(
        name = kwarg[0],
        code = kwarg[1].source if isinstance(kwarg[1], literal) else kwarg[1],
        value_xml_node = expr_xml_node(kwarg[1])
      )
      for kwarg in all_kwargs
    )

  return ArgList(all_args)

def make_kwargs(code: str, kwarg_xml_nodes: list[Element]) -> list[KWArg]:
  """Return KWArg(s) based on <keyword> XML Element(s)

  Parameters
  ----------
  code : str
      the source code text
  kwarg_xml_nodes : list[Element]
      list of XML Elements representing keyword

  Returns
  -------
  list[KWArg]
      a list of KWArgs representing those keywords
  """
  code_kwargs_list = []
  for kwarg_node in kwarg_xml_nodes:
    # keyword argument name
    kwarg_names = [
      x.text for x in kwarg_node.xpath("./arg")
    ]

    # get the textual form for values
    kwarg_values = [v for v in kwarg_node.xpath("./value/*")]
    kwargs_values_strings = [
      get_node_source(code, kw).decode()
      for kw in kwarg_values
    ]

    # combine them into pairs
    kwargs_pairs = list(zip(kwarg_names, kwargs_values_strings))

    # construct the list of Arg(s) from the keyword pairs
    code_kwargs_list.append([
      KWArg(
        name = k,
        code = v,
        value_xml_node = expr_xml_node(v),
        keyword_xml_node = kwarg_node
      )
      for k, v in kwargs_pairs
    ])
  return flatten_list(code_kwargs_list)

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
  xml_tree = xml(gcf.source) if isinstance(code, GradeCodeFound) else xml(code)

  request_type = 'arguments'
  # TODO create a __str__ representation for ArgList
  request = ''
  results = []

  # Note: we have to encode the code to escape it properly
  match_args = match.args

  # if there are no arguments to look for in particular, look for
  # all of the arguments in code
  if match_args is None:
    results = [
      x_tree.xpath("./args/*|./keywords/*")
      for x_tree in xml_tree.xpath(".//Call")
    ]
    results = list(itertools.chain(*results))
  else:
    # Extracting each keyword pair is a bit tricky because a value
    # could be any ast node so there is no way to have one query
    # satisfy all types of nodes. So, instead we look at the
    # <keyword> and its <value> node source text to reconstruct them.
    # TODO if a gcf was passed when there was a previous request
    # we need to iterate through gcf.results to repeat this process
    # so we can make all of the Arg/KWArg 
    all_call_xml_nodes = xml_tree.xpath(".//Call")
    
    # extract the positional args
    all_arg_xml_nodes = flatten_list([
      call.xpath("./args/*")
      for call in all_call_xml_nodes
    ])
    # extract the kwargs args
    all_kwarg_xml_nodes = flatten_list([
      call.xpath("./keywords/*")
      for call in all_call_xml_nodes
    ])

    # construct Arg() for positional arguments
    code_args_list = [
      Arg(
        code = get_node_source(code, arg).decode(),
        xml_node = copy(arg)
      )
      for arg in all_arg_xml_nodes
    ]

    # extract the keyword args
    code_kwargs_list = make_kwargs(code, all_kwarg_xml_nodes)
    # combine the args with the kwargs
    all_code_args = code_args_list + code_kwargs_list
      
    # check that each match Arg is in code's [Arg]
    results = get_matched_arguments(match_args, all_code_args)

  # TODO make the chaining work well
  return gcf.push(request_type=request_type, request=request, result=results)

def get_matched_arguments(
  match_args: list[Arg | KWArg],
  all_code_args: list[Arg | KWArg]
 ) -> list[Element]:
  """Return all code XML elements that match given the list of match and code arguments.

  Parameters
  ----------
  match_args : list[Arg  |  KWArg]
      a list with Arg and KWArgs representing positional and keyword arguments
      to match against
  all_code_args : list[Arg  |  KWArg]
      a list with Arg and KWArgs representing positional and keyword arguments
      of the code

  Returns
  -------
  list[Element]
      a list of XML Element(s)
  """
  results = []
  for match_arg in match_args:
    # for argument, element in args_spec:
    for argument in all_code_args:
      # if match Arg Element is the same as the code Arg Element
      # add the code Arg Element as a result
      if type(match_arg) != type(argument):
        continue
      elif isinstance(match_arg, KWArg) and isinstance(argument, KWArg):
        # if we're comparing keyword arguments 
        # check value nodes match
        value_nodes_match = compare_xml_nodes(
          match_arg.value_xml_node,
          argument.value_xml_node
        )
        # check the kwarg name too
        arg_names_match = match_arg.name == argument.name

        if value_nodes_match and arg_names_match:
          results.append(argument.keyword_xml_node)
      elif compare_xml_nodes(match_arg.xml_node, argument.xml_node):
        results.append(argument.xml_node)
  return results

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
