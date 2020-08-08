
import unittest

from pygradethis.conditions import *
from pygradethis.python_grader import *

class PythonGraderTest(unittest.TestCase):

    # Grade result -------------------------------------

    def test_pass_if_correct(self):
        result = grade(
            python_pass_if(2, "Woah, nice!"),
            user_code="2", 
            solution_code="2", 
        )
        self.assertTrue(result['correct'])
        self.assertEqual(result['type'], "success")

    def test_pass_if_incorrect(self):
        result = grade(
            python_pass_if(2, "Woah, nice!"),
            user_code="1", 
            solution_code="2", 
        )
        self.assertFalse(result['correct'])
        self.assertEqual(result['type'], "error")
    
    def test_multiple_pass_if_correct(self):
        result = grade(
            python_pass_if(2, "Woah, nice!"),
            python_pass_if(3, "Piece of cake!"),
            user_code="3",
        )
        self.assertTrue(result['correct'])
        self.assertEqual(result['type'], "success")
    
    def test_multiple_pass_if_incorrect(self):
        result = grade(
            python_pass_if(2, "Woah, nice!"),
            python_pass_if(3, "Piece of cake!"),
            user_code="1",
        )
        self.assertFalse(result['correct'])
        self.assertEqual(result['type'], "error")

    def test_pass_if_fail_if_correct(self):
        result = grade(
            python_pass_if(2, "Noice!"),
            python_fail_if(1, "We do not want 1."),
            user_code="2",
            solution_code="2", 
        )
        self.assertTrue(result['correct'])
        self.assertEqual(result['type'], "success")

    def test_pass_if_fail_if_incorrect(self):
        result = grade(
            python_pass_if(2, "Noice!"),
            python_fail_if(1, "We do not want 1."),
            user_code="1",
            solution_code="2", 
        )
        self.assertFalse(result['correct'])
        self.assertEqual(result['type'], "error")

    def test_fail_if_correct(self):
        # single fail_if; if user don't match any fail_ifs, count as correct by default
        result = grade(
            python_fail_if(1, "We wanted 1."),
            user_code="3",
        )
        self.assertTrue(result['correct'])
        self.assertEqual(result['type'], "success")
    
    def test_fail_if_incorrect(self):
        result = grade(
            python_fail_if(1, "We wanted 1."),
            user_code="1",
        )
        self.assertFalse(result['correct'])
        self.assertEqual(result['type'], "error")

    def test_fail_ifs_correct(self):
        # multiple fail_ifs; if user don't match any fail_ifs, count as correct by default
        result = grade(
            python_fail_if(1, "We do not want 1."),
            python_fail_if(2, "We do not want 2."),
            user_code="3",
        )
        self.assertTrue(result['correct'])
        self.assertEqual(result['type'], "success")
    
    def test_fail_ifs_incorrect(self):
        result = grade(
            python_fail_if(1, "We do not want 1."),
            python_fail_if(2, "We do not want 2."),
            user_code="2",
        )
        self.assertFalse(result['correct'])
        self.assertEqual(result['type'], "error")
    
    # Grade code -------------------------------------
    # TODO add static code check examples
    

if __name__ == "__main__":
    unittest.main()