from textwrap import dedent
from lxml.etree import _Element as Element

from pygradecode.find_attributes import (
  find_attributes, find_properties, get_method_chains
)
from pygradecode.grade_code_found import GradeCodeFound

def test_find_attributes_simple():
  code_with_attrs = dedent(
    """
    df.head()
    df.shape
    df.empty
    """
  ).strip()

  found = find_attributes(code_with_attrs)
  results = found.last_result

  assert len(results) == 3
  assert all(isinstance(e, Element) for e in results)

  assert results[0].tag == 'Call'
  assert results[1].tag == 'Expr'
  assert results[2].tag == 'Expr'

def test_find_attributes_complex():
  code_with_attrs = dedent(
    """
    (penguins
      .loc[penguins['species'] == 'Chinstrap']
      .assign(rel_year = lambda df_: df_['year'] - 2007)
      .loc[lambda df_: df_['rel_year'] < 2]
    )
    penguins.shape
    """
  ).strip()

  found = find_attributes(code_with_attrs)
  results = found.last_result

  assert len(results) == 4
  assert all(isinstance(e, Element) for e in results)

  assert results[0].tag == 'Subscript'
  assert results[1].tag == 'Call'
  assert results[2].tag == 'Subscript'
  assert results[3].tag == 'Expr'

def test_find_properties():
  code_with_props = dedent(
    """
    df.shape
    df.empty
    """
  ).strip()

  found = find_properties(code_with_props)
  results = found.last_result

  assert len(results) == 2
  assert all(isinstance(e, Element) for e in results)

  assert results[0].tag == 'Expr'
  assert results[1].tag == 'Expr'
  
  code_without_props = dedent(
    """
    df.head()
    df.loc[:, 'foo']
    """
  ).strip()

  found = find_properties(code_without_props)
  results = found.last_result

  assert len(results) == 0

def test_find_properties_match():
  code_with_props = dedent(
    """
    df.head()
    df.empty
    df.loc[:,'foo']
    df.shape
    """
  ).strip()

  found = find_properties(code_with_props, match="empty")
  results = found.last_result

  assert len(results) == 1
  assert results[0].tag == 'Expr'

  found = find_properties(code_with_props, match="shape")
  results = found.last_result

  assert len(results) == 1
  assert results[0].tag == 'Expr'

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

  non_chained_code = dedent(
    """
    penguins.loc[:, "bill_length_mm"]
    penguins.nlargest(3)
    """   
  ).strip()

  method_chains = get_method_chains(non_chained_code)
  assert len(method_chains) == 0
