# core
import sys
from io import StringIO
from itertools import zip_longest
from collections import namedtuple
from typing import Any, Tuple

from .conditions import GraderCondition
# testing
import unittest
try:
    # attempt to import `pandas` related asserts
    from pandas.testing import assert_frame_equal, assert_series_equal
except:
    pass

class TestCondition(unittest.TestCase):
    """Custom TestCase to do asserts on GraderCondition(s) and incorporate
    custom asserts from libraries like pandas for dataframe checking.
    """
    def __init__(self, test_name: str, condition: GraderCondition):
        super(TestCondition, self).__init__(test_name)
        self.condition = condition
        
    ## Test Case for `GraderCondition`
    def test_condition(self):
        ID, actual, expected = self.condition
        try:
            if (
                actual.__class__.__name__ == "DataFrame" and 
                expected.__class__.__name__ == "DataFrame" and
                "pandas" in sys.modules
            ):
                self.assertTrue(assert_frame_equal(actual, expected))
            self.assertEqual(actual, expected)
        except Exception:
            # Note: this ID isn't really being used at the moment for error
            # checking
            self.fail(ID)

# we want custom result for `TextTestRunner`
class ConditionTestResult(unittest.TextTestResult):
    """Custom test result where we maintained a matched test ID list to reference
    later when determining matched conditions.
    """
    def __init__(self, stream, descriptions: bool, verbosity: int):
        super(ConditionTestResult, self).__init__(stream, descriptions, verbosity)
        self.matched = []

    def addSuccess(self, test: TestCondition):
        super(ConditionTestResult, self).addSuccess(test)
        # add matched case
        self.matched.append(test.condition.id)

def test_conditions(*conditions: GraderCondition, 
                    user_result: Any = None, 
                    default_correct: bool = False,
                    deafult_message: str = "",
                    r: dict = {}) -> Tuple[bool, GraderCondition]:
    # create a test suite
    suite = unittest.TestSuite()
    # convenience tuple for structuring test cases
    TestCase = namedtuple("TestCase", ["id", "actual", "expected"])
    # make TestCondition based on GradeCondition(s)
    for i, c in enumerate(conditions):
        suite.addTest(
            TestCondition(
                'test_condition', TestCase(i, user_result, c['x'])
            )
        )
    # capture current sys.stderr buffer (default one)
    default_buffer = sys.stderr
    # capture test print output for AssertionError(s)
    sys.stderr = StringIO()
    # run suite
    results = unittest.TextTestRunner(resultclass = ConditionTestResult).run(suite)
    # restore stderr to buffer so we catch any errors on our matching code below
    sys.stderr = default_buffer
    
    # get matched conditions by subsetting conditions list with matched index list
    matched_conditions = list(map(lambda i: conditions[i], results.matched))
    incorrect_match = None
    if len(matched_conditions) > 0:
        # return on the first `python_pass_if`
        for mc in matched_conditions:
            if mc['correct']:
                return True, mc
            elif incorrect_match == None:
                # keep record of the first `python_fail_if` to return
                incorrect_match = mc
    else: # no match
        # - if there is at least one pass_if() condition, then default to an incorrect grade 
        # - otherwise, we default to a correct grade
        if len([c for c in conditions if c['correct']]) != 0:
            return default_correct, None
        # otherwise if we only have fail_ifs, we default to a correct grade 
        elif len([c for c in conditions if not c['correct']]) != 0:
            return True, None
    return default_correct, incorrect_match
