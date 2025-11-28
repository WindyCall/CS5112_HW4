import unittest
import sys
sys.path.append("..")


from problem_2.p2_a import linear_search 

class TestProblem1(unittest.TestCase):
  def test_correctness_public_a1(self):
    """Public test """
    boxes = [[4,8],[2,8]]
    packages = [2,3,5]
    self.assertEqual(linear_search(packages, boxes), 6)

  def test_correctness_public_a2(self):
    """Public test """
    boxes = [[1,4],[2,3],[3,4]]
    packages = [2,3,5]
    self.assertEqual(linear_search(packages, boxes), -1)

  def test_correctness_public_a3(self):
    """Public test """
    boxes = [[12],[11,9],[10,5,14]]
    packages = [3,5,8,10,11,12]
    self.assertEqual(linear_search(packages, boxes), 9)

  def test_correctness_public_a4(self):
    """Public test """
    boxes = [[3], [2, 4], [1, 5, 6]]
    packages = [3]
    self.assertEqual(linear_search(packages, boxes), 0) 

  def test_correctness_public_a5(self):
    """Public test """
    boxes = [[4, 6, 8], [3, 5, 7, 9]]
    packages = [3, 5, 7]
    self.assertEqual(linear_search(packages, boxes), 0)
  
  def test_correctness_public_a6(self):
    """Public test """
    boxes = [[1, 2], [2, 3, 4], [3, 5]]
    packages = [1, 2, 6]
    self.assertEqual(linear_search(packages, boxes), -1)
  
  def test_correctness_public_a7(self):
    """Public test """
    boxes = [[5, 7], [10, 15, 20], [6, 8]]
    packages = [5, 10]
    self.assertEqual(linear_search(packages, boxes), 5)

  def test_correctness_public_a8(self):
    """Public test """
    boxes = [[2, 3], [1, 4], [5, 6]]
    packages = [7, 8, 9]
    self.assertEqual(linear_search(packages, boxes), -1)
  



if __name__ == '__main__':
  unittest.main()