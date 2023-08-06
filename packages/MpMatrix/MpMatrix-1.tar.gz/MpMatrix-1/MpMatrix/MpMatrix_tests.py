import unittest
from MpMatrix import *


class MyTestCase(unittest.TestCase):
    def test_add_01(self):
        a: MpMatrix = MpMatrix([[1, 2], [3, 4]])
        b: MpMatrix = MpMatrix([[5, 6], [7, 8]])
        self.assertEqual(a + b, MpMatrix([[6, 8], [10, 12]]))

    def test_add_02(self):
        a: MpMatrix = MpMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        b: MpMatrix = MpMatrix([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
        self.assertEqual(a + b, MpMatrix([[10, 10, 10], [10, 10, 10], [10, 10, 10]]))

    def test_add_03(self):
        a: MpMatrix = MpMatrix([[1, 2]])
        b: MpMatrix = MpMatrix([[2, 3]])
        c: MpMatrix = MpMatrix([[3, 4]])
        self.assertEqual(a + b + c, MpMatrix([[6, 9]]))

    def test_sub_01(self):
        a: MpMatrix = MpMatrix([[7, 5]])
        b: MpMatrix = MpMatrix([[5, 3]])
        self.assertEqual(a - b, MpMatrix([[2, 2]]))

    def test_sub_02(self):
        a: MpMatrix = MpMatrix([[7, 5], [6, 3]])
        b: MpMatrix = MpMatrix([[5, 3], [4, 7]])
        self.assertEqual(a - b, MpMatrix([[2, 2], [2, -4]]))

    def test_sub_03(self):
        a: MpMatrix = MpMatrix([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
        b: MpMatrix = MpMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertEqual(a - b, MpMatrix([[8, 6, 4], [2, 0, -2], [-4, -6, -8]]))

    def test_mul_01(self):
        a: MpMatrix = MpMatrix([[3, 2, 1], [5, 6, 3]])
        b: MpMatrix = MpMatrix([[4, 1], [5, 2], [3, 3]])
        self.assertEqual(a * b, MpMatrix([[25, 10], [59, 26]]))

    def test_mul_02(self):
        a: MpMatrix = MpMatrix([[3, 4]])
        b: MpMatrix = MpMatrix([[6], [2]])
        self.assertEqual(a * b, MpMatrix([[26]]))

    def test_mul_03(self):
        a: MpMatrix = MpMatrix([[mpf("4.12"), mpf("6.13")]])
        b: MpMatrix = MpMatrix([[mpf("23.33")], [mpf("13.28")]])
        self.assertEqual(a * b, MpMatrix([[mpf("177.526")]]))
        
    def test_mul_04(self):
        a: MpMatrix = MpMatrix([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
        b: MpMatrix = MpMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertEqual(a * b, MpMatrix([[90.0, 114.0, 138.0], [54.0, 69.0, 84.0], [18.0, 24.0, 30.0]]))


if __name__ == '__main__':
    unittest.main()
