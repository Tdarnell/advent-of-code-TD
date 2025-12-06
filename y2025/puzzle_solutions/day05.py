#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
File: day05.py
Project: advent-of-code
File Created: Saturday, 6th December 2025 12:11:04 pm
Author: tdarnell (tdarnell@users.noreply.github.com)
-----
Last Modified: Saturday, 6th December 2025 12:25:35 pm
Modified By: tdarnell (tdarnell@users.noreply.github.com>)
-----
HISTORY:
Date      	By	Comments
----------	---	---------------------------------------------------------
"""

import logging
from pathlib import Path
import re


try:
    from .common_utils import log_execution_time, set_up_logger, read_day_input
except (ImportError, ValueError):
    from common_utils import log_execution_time, set_up_logger, read_day_input

LOGGER: logging.Logger = set_up_logger(
    day=int(Path(__file__).stem[3:]),
    folder=str(Path(__file__).resolve().parent.parent / "logs"),
)


@log_execution_time(logger=LOGGER)
def day05_part1(
    input_str: str = "3-5\n10-14\n16-20\n12-18\n\n1\n5\n8\n11\n17\n32",
) -> int:
    fresh_range, to_check = input_str.split("\n\n")
    fresh_stop_starts = [
        tuple(map(int, re.findall(r"\d+", line))) for line in fresh_range.splitlines()
    ]
    fresh_count = 0
    # I made the mistake of first creating a flattened list of integers here
    # without looking at the size of the numbers in the input ...
    # This crashed my interpreter as they are large integer ranges so
    # I swapped to a < > comparison
    #
    # I can already see a better solution to this problem with numpy by building
    # an array of starts and an array of stops and doing the comparison logic
    # on both arrays vectorized, then seeing if I had a True from both arrays.
    # I will implement that as a seperate function so my original is retained.
    for idx in to_check.splitlines():
        num = int(idx)
        for start, stop in fresh_stop_starts:
            if start <= num <= stop:
                fresh_count += 1
                break
    return fresh_count


@log_execution_time(logger=LOGGER)
def day05_part2(
    input_str: str = "3-5\n10-14\n16-20\n12-18\n\n1\n5\n8\n11\n17\n32",
):
    # this part is really simple, I will do the same as above and subtract the start from the stop
    # then sum for each
    #
    # again I can see how numpy would speed this up.
    #
    # Ah, I did not consider overlaps!
    fresh_range, to_check = input_str.split("\n\n")
    fresh_stop_starts = [
        tuple(map(int, re.findall(r"\d+", line))) for line in fresh_range.splitlines()
    ]
    # first I need to loop through and consolidate any overlapping ranges
    fresh_stop_starts.sort()
    consolidated_ranges = []
    current_start, current_stop = fresh_stop_starts[0]
    for start, stop in fresh_stop_starts[1:]:
        if start <= current_stop:
            # This one is overlapping another
            current_stop = max(current_stop, stop)
        else:
            consolidated_ranges.append((current_start, current_stop))
            current_start, current_stop = start, stop
    consolidated_ranges.append((current_start, current_stop))
    total = 0
    for rng in consolidated_ranges:
        total += rng[1] + 1 - rng[0]
    return total


if __name__ == "__main__":
    expected_solution = 3
    got_solution = day05_part1()
    if expected_solution != got_solution:
        LOGGER.error(
            f"Problem with solution to part 1! Did not get the expected answer of {expected_solution} for the provided worked example. Instead got: {got_solution}"
        )

    input_str = read_day_input(
        day=5, folder=Path(__file__).resolve().parent.parent / "inputs"
    )
    part1_solution: int = day05_part1(input_str)
    LOGGER.info(f"Part 1 solution: {part1_solution}")

    expected_solution = 14
    got_solution = day05_part2()
    if expected_solution != got_solution:
        LOGGER.error(
            f"Problem with solution to part 2! Did not get the expected answer of {expected_solution} for the provided worked example. Instead got: {got_solution}"
        )

    part2_solution: int = day05_part2(input_str)
    LOGGER.info(f"Part 2 solution: {part2_solution}")
