import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from puzzle_solutions.day02 import day02_part1, day02_part2


class TestDay02Methods(unittest.TestCase):
    def test_part1_default(self):
        self.assertEqual(day02_part1(), 1227775554)

    def test_part1_custom(self):
        self.assertEqual(day02_part1("11-11"), 11)
        self.assertEqual(day02_part1("12-13"), 0)
        self.assertEqual(day02_part1("10-22"), 11 + 22)
        self.assertEqual(day02_part1("5-3"), 0)
        self.assertEqual(day02_part1("notarange"), 0)

    def test_part2_default(self):
        self.assertEqual(day02_part2(), 4174379265)

    def test_part2_custom(self):
        self.assertEqual(day02_part2("11-22"), 11 + 22)
        self.assertEqual(day02_part2("12-13"), 0)
        self.assertEqual(day02_part2("1212-1212"), 1212)
        self.assertEqual(day02_part2("123123-123123"), 123123)
        self.assertEqual(day02_part2("5-3"), 0)
        self.assertEqual(day02_part2("notarange"), 0)


if __name__ == "__main__":
    unittest.main()
