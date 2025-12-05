import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from puzzle_solutions.day03 import day03_part1, day03_part2


class TestDay03Methods(unittest.TestCase):
    def test_part1_example(self):
        # default example from the function should return 357
        self.assertEqual(day03_part1(), 357)

    def test_part1_empty_input(self):
        # empty input should return 0 or appropriate value
        self.assertEqual(day03_part1(""), 0)

    def test_part1_large_Examples(self):
        self.assertEqual(
            day03_part1(
                """3223323232423342133321323321133325222233342332323323343713331321434231231232333333232334233323322122
3422323123349134332433333333432333313333323413433133433343234433433334323333452433843344143323335344
3323113221321312236523622222221222225424323212132242333365351332221432232235143422248222121121832228
3463333333523444333334433344544335323235227453444243335438244443585333243345323433342343323423544343
4233366944836552382823534346549355354476555367335594833663342368343653554644862935563623533154857355
1332332433331354333343732343231333333333333244331233163343322313323333333342353333433313332343313344
2323333333132333133423233333532331333334313243333333432343123323232442532313323213333333223533324332"""
            ),
            74 + 98 + 88 + 88 + 99 + 76 + 55,
        )

    def test_part2_example(self):
        # default example from the function should return 3121910778619
        self.assertEqual(day03_part2(), 3121910778619)

    def test_part2_empty_input(self):
        # empty input should return 0 or appropriate value
        self.assertEqual(day03_part2(""), 0)


if __name__ == "__main__":
    unittest.main()
