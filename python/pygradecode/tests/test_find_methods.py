from textwrap import dedent
from lxml.etree import _Element as Element

from pygradecode.find_methods import (
  find_methods, get_method_chains
)
from pygradecode.grade_code_found import GradeCodeFound

def test_get_method_chains():
  chained_code = dedent(
    """
    (penguins
      .loc[:, "bill_length_mm"]
      .nlargest(3)
    )
    """   
  ).strip()
  
  method_chains = get_method_chains(chained_code)
  
  assert len(method_chains) == 1
  assert all(isinstance(e, Element) for e in method_chains)
  assert all(e.tag == 'Attribute' for e in method_chains)

  # function calls that are not nested
  non_chained_code = dedent(
    """
    penguins.loc[:, "bill_length_mm"]
    penguins.nlargest(3)
    """   
  ).strip()

  method_chains = get_method_chains(non_chained_code)
  assert len(method_chains) == 0
