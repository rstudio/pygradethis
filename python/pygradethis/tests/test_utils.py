from pygradethis.utils import get_last_value, get_envir_diff, NONE
import pandas as pd
from pandas.testing import assert_frame_equal

def test_get_last_value_exprs():
  envir, last_value = get_last_value("x = 2\nx + 1", {})
  assert last_value == 3

  envir, last_value = get_last_value("def foo(x):\n\treturn x + 1\nfoo(1)", {})
  assert last_value == 2

  envir, last_value = get_last_value("import pandas as pd\npd.DataFrame({'a':[1,2,3]})", {})
  assert_frame_equal(last_value, pd.DataFrame({'a':[1,2,3]}))

def test_get_last_value_statement():
  envir, last_value = get_last_value("2 + 2\nx = 2", {})
  assert last_value != None
  assert last_value == NONE

  envir, last_value = get_last_value("2 + 2\nNone", {})
  assert last_value == None
  assert last_value != NONE

def test_get_envir_diff():
  envir_prep = {'x': 2}
  envir_result = {'x': 2, 'y': 4}
  assert get_envir_diff(envir_prep, envir_result) == ['y']