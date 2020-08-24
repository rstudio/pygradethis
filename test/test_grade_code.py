
import unittest

from pygradethis.grade_code import grade_code

class GradeCodeTest(unittest.TestCase):

    def test_core(self):
        test_cases = [
            # different core types
            ("\"1\"", "1", "I expected 1, but what you wrote was interpreted as \"1\" at line 1."),
            ("1", "\"1\"", "I expected \"1\", but what you wrote was interpreted as 1 at line 1."),
            ("[1]", "\"1\"", "I expected \"1\", but what you wrote was interpreted as [1] at line 1."),
            ("True", "\"1\"", "I expected \"1\", but what you wrote was interpreted as True at line 1."),
            ("False", "\"1\"", "I expected \"1\", but what you wrote was interpreted as False at line 1."),
            # str vs str
            ("\"not hello\"", "\"hello\"", "I expected \"hello\", but what you wrote was interpreted as \"not hello\" at line 1."),
            # list vs list
            ("[2]", "[]", "I did not expect 2 at line 1."),
            ("[1,2]", "[1]", "I did not expect 2 at line 1."),
            ("[1]", "[1,2]", "I expected 2 at line 1."),
            # expr vs something else
            ("1 + 1", "1", "I expected 1, but what you wrote was interpreted as 1 + 1 at line 1."),
            ("1 + (2 + 2)", "1 + (2 + 3)", "I expected 3, but what you wrote was interpreted as 2 in 2 + 2 at line 1."),
            ("-1", "1", "I expected 1, but what you wrote was interpreted as -1 at line 1."),
            # add more...
        ]
        for t in test_cases:
            message = grade_code(t[0], t[1])
            self.assertEqual(message, t[2], (
                    "Failed test case!\nUser:{}\nSolution:{}\nExpected:{}\nGot:{}".format(
                        t[0],
                        t[1],
                        t[2],
                        message
                    )
                )
            )
    
    def test_functions(self):
        test_cases = [
            ("2 + sum([1,2])", "2 + sum([1,1])", "I expected sum(iterable=[1, 1], start=0), but what you wrote was interpreted as sum(iterable=[1, 2], start=0) at line 1."),
            ("sqrt(log(2))", "sqrt(log(1))", "I expected 1, but what you wrote was interpreted as 2 in log(2) at line 1."),
            ("def foo(a, b=1): pass; foo(2)", "def foo(a, b=1): pass; foo(1)", "I expected foo(a=1, b=1), but what you wrote was interpreted as foo(a=2, b=1) at line 1."),
            ("def foo(a, b=1): pass; foo(a=2)", "def foo(a, b=1): pass; foo(1)", "I expected foo(a=1, b=1), but what you wrote was interpreted as foo(a=2, b=1) at line 1."),
            ("def foo(a, b=1): pass; foo(a=[2])", "def foo(a, b=1): pass; foo(2, 2)", "I expected foo(a=2, b=2), but what you wrote was interpreted as foo(a=[2], b=1) at line 1."),
            ("def foo(a, b=1): pass; foo(a=\"2\", b=2)", "def foo(a, b=1): pass; foo(2, 2)", "I expected foo(a=2, b=2), but what you wrote was interpreted as foo(a=\"2\", b=2) at line 1."),
            ("def head(n=5): pass; head(12)", "def head(n=5): pass; head(n=10)", "I expected head(n=10), but what you wrote was interpreted as head(n=12) at line 1."),
            # add more...
        ]
        for t in test_cases:
            message = grade_code(t[0], t[1])
            self.assertEqual(message, t[2], (
                    "Failed test case!\nUser:{}\nSolution:{}\nExpected:{}\nGot:{}".format(
                        t[0],
                        t[1],
                        t[2],
                        message
                    )
                )
            )
    
if __name__ == "__main__":
    unittest.main()

