import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from puzzle_solutions.day01 import (
    day01_part1_for_loop_method,
    day01_part1_vectorized,
    day01_part2_for_loop_method,
)


class TestDay01Methods(unittest.TestCase):
    def test_example_returns_3(self):
        # default example from the functions should return 3
        self.assertEqual(day01_part1_for_loop_method(), 3)
        self.assertEqual(day01_part1_vectorized(), 3)

    def test_empty_input_returns_0(self):
        # empty input should return 0
        self.assertEqual(day01_part1_for_loop_method(""), 0)
        self.assertEqual(day01_part1_vectorized(""), 0)

    def test_single_rotation_wraps_to_zero(self):
        # Start at 50, R50 -> (50 + 50) % 100 == 0
        self.assertEqual(day01_part1_for_loop_method("R50"), 1)
        self.assertEqual(day01_part1_vectorized("R50"), 1)

    def test_multiple_zeros_counted(self):
        # Start at 50, R50 -> 0, then R100 -> 0 again => two zeros
        self.assertEqual(day01_part1_for_loop_method("R50\nR100"), 2)
        self.assertEqual(day01_part1_vectorized("R50\nR100"), 2)

    def test_part2_example_returns_6(self):
        # default example from the function should return 6
        self.assertEqual(day01_part2_for_loop_method(), 6)

    def test_part2_empty_input_returns_0(self):
        # empty input should return 0
        self.assertEqual(day01_part2_for_loop_method(""), 0)

    def test_part2_single_rotation_wraps_to_zero(self):
        # Start at 50, R50 -> (50 + 50) == 100, so one wrap
        self.assertEqual(day01_part2_for_loop_method("R50"), 1)

    def test_part2_multiple_wraps(self):
        # Start at 50, R50 -> 100 (1 wrap), R100 -> 200 (2 wraps)
        self.assertEqual(day01_part2_for_loop_method("R50\nR100"), 2)


if __name__ == "__main__":
    unittest.main()
