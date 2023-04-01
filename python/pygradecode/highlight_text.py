"""Functions that format and style various objects to pretty print."""

import builtins
from dataclasses import dataclass
from functools import singledispatch
from rich.console import Console

@singledispatch
def my_print(arg):
  builtins.print(arg)

@dataclass
class FormattedText:
  text: str

@my_print.register
def _(arg: FormattedText, console: Console = Console(color_system='standard')):
  console.print(arg.text)

# Override the default print() with my_print
print = my_print

def format_text(
  code: str, target_node,
  console: Console = Console(color_system='standard')
) -> str:
  location = target_node.attrib
  end_line = int(location['end_lineno']) - 1

  code_lines = code.splitlines()

  # get the target line
  # NOTE: we might have different heuristics for different types of nodes
  # but generally when a particular node spans multiple lines
  # it might suffice to just focus on the most pertinent lines instead
  # of highlight blocks of code
  target_line = code_lines[end_line]

  # get column offset
  col_start = int(location['col_offset'])
  col_end = int(location['end_col_offset'])

  # beginning string is all previous lines
  prev_str = "\n".join(code_lines[:end_line])
  
  beginning_line_str = target_line[:col_start]
  formatted_str = (
    "[u bold]" + 
    target_line[col_start] + 
    target_line[col_start + 1:col_end] + 
    "[/u bold]"
  )
  end_line_str = target_line[col_end:]

  # end string is the rest of the lines

  remaining_str = "\n".join(code_lines[end_line + 1:])

  return FormattedText(
    f"{prev_str}\n{beginning_line_str}{formatted_str}{end_line_str}\n{remaining_str}"
  )
