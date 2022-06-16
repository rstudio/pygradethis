# core
import sys
from io import StringIO
from itertools import zip_longest
from collections import namedtuple
from typing import Any, Tuple

from .conditions import Graded
# testing
import unittest
try:
    # attempt to import `pandas` related asserts
    from pandas.testing import assert_frame_equal, assert_series_equal
except:
    pass

class TestCondition(unittest.TestCase):
    """Custom TestCase to do asserts on Graded(s) and incorporate
    custom asserts from libraries like pandas for dataframe checking.
    """
    def __init__(self, test_name: str, condition: Graded):
        super(TestCondition, self).__init__(test_name)
        self.condition = condition
        
    ## Test Case for `Graded`
    def test_condition(self):
        # Note: currently the `correct` field from TestCase tuple isn't used
        # and is only included to avoid a tuple unpacking error
        ID, actual, expected, correct = self.condition
        try:
            if (actual.__class__.__name__ == "DataFrame" and 
                expected.__class__.__name__ == "DataFrame" and
                "pandas" in sys.modules):
                assert_frame_equal(actual, expected)
            else:
                # skip if it's a plain pass or fail condition
                if expected is None:
                    pass
                else:
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
        self.num_correct = 0

    def addSuccess(self, test: TestCondition):
        super(ConditionTestResult, self).addSuccess(test)
        # add matched case
        self.matched.append(test.condition.id)
        if test.condition.correct:
            self.num_correct += 1

def test_conditions(*conditions: Graded, 
                    user_result: Any = None) -> Tuple[bool, Graded]:
    # create a test suite
    suite = unittest.TestSuite()
    # convenience tuple for structuring test cases
    TestCase = namedtuple("TestCase", ["id", "actual", "expected", "correct"])
    # make TestCondition based on GradeCondition(s)
    for i, c in enumerate(conditions):
        suite.addTest(
            TestCondition(
                'test_condition', TestCase(i, user_result, c['x'], c['correct'])
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
        # return on the first `pass_if_equals`
        for mc in matched_conditions:
            if mc['correct']:
                return mc
            elif incorrect_match == None:
                # keep record of the first `fail_if_equals` to return (if any)
                incorrect_match = mc
    else: # no match
        # for now just return failing
        # we will need to revisit the grading flow later to handle cases where there are no
        # matching grading conditions
        return Graded(
                x = None,
                message = "",
                correct = False,
                type = "error"
            )
    return incorrect_match
