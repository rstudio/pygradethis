import sys
from io import StringIO
from itertools import zip_longest

from pygradethis.conditions import python_pass_if, python_fail_if

import unittest
from pandas.testing import assert_frame_equal, assert_series_equal

class TestCondition(unittest.TestCase):

    def __init__(self, test_name, condition):
        super(TestCondition, self).__init__(test_name)
        self.condition = condition
        
    ## Test Case for `GraderCondition`
    def test_condition(self):
        actual, expected = self.condition
        try:
            if type(actual).__name__ == "DataFrame" and type(expected).__name__ == "DataFrame":
                self.assertTrue(assert_frame_equal(actual, expected))
            self.assertEqual(actual, expected)
        except Exception:
            self.fail()

if __name__ == '__main__':
    sys.stderr = StringIO()     # capture output
    # create a test suite
    suite = unittest.TestSuite()

    # TODO try to make TestCondition based on GradeCondition(s)
    conditions = [
        python_pass_if("1", "1 is correct!"),
        python_pass_if(2, "2 is correct!"),
        python_fail_if(1, "1 is incorrect!"),
        python_fail_if("3", "3 is incorrect!"),
    ]
    cases = [
        TestCondition('test_condition', ("1", "1")),
        TestCondition('test_condition', (2, 2)),
        TestCondition('test_condition', (2, 2)),
        TestCondition('test_condition', ("3", "3"))
    ]
    # add test cases
    for c in cases:
        suite.addTest(c)
    # run suite
    results = unittest.TextTestRunner().run(suite)
    print("# unmatched conditions: {}".format(len(results.failures)))

    # TODO matching logic can be incorporated here
    for i, (case, failure) in enumerate(zip_longest(cases, results.failures, fillvalue="")):
        # print(type(case), type(failure))
        if failure == "":
            print("{} matched!".format(conditions[i]))
        else:
            print("{} didn't match!".format(conditions[i]))

