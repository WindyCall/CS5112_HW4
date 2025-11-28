import unittest
import json
import sys
sys.path.append("..")

from problem_3.p3_b import count_min_sketch

class TestProblem3(unittest.TestCase):
    ### Public test for 3b
    def test_simple(self):
        test_problems = [
            ([1,2], [3,5], 100, 3, [10,11,10], [[0, 2, 1], [1, 2, 0]]),
            ([2,3,2,5], [1,10,200,4], 9, 4, [129,  56, 117, 142,  82, 161, 114,  68, 161, 149], [[3, 2, 3, 2], [2, 3, 0, 5], [4, 1, 2, 3], [4, 2, 2, 2]]),
        ]
        for test in test_problems:
            ans = test[-1]
            self.assertListEqual(
                count_min_sketch(a=test[0], b=test[1], p=test[2], w=test[3], stream=iter(test[4])), ans)

    def test_complex(self):
        with open("tests/inputs/p3_inputs.json", "rt") as f:
            test_problems = json.load(f)

        for test in test_problems:
            ans = test['ans']
            self.assertListEqual(
                count_min_sketch(a=test['a'], b=test['b'], p=test['p'], w=test['w'], stream=iter(test['stream'])), 
                ans)


if __name__ == '__main__':
    unittest.main()
