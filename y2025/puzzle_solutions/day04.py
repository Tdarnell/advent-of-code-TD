#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
File: day04.py
Project: advent-of-code
File Created: Saturday, 6th December 2025 11:33:44 am
Author: tdarnell (tdarnell@users.noreply.github.com)
-----
Last Modified: Saturday, 6th December 2025 11:56:26 am
Modified By: tdarnell (tdarnell@users.noreply.github.com>)
-----
HISTORY:
Date      	By	Comments
----------	---	---------------------------------------------------------
"""

import logging
from pathlib import Path


try:
    from .common_utils import log_execution_time, set_up_logger, read_day_input
except (ImportError, ValueError):
    from common_utils import log_execution_time, set_up_logger, read_day_input

LOGGER: logging.Logger = set_up_logger(
    day=int(Path(__file__).stem[3:]),
    folder=str(Path(__file__).resolve().parent.parent / "logs"),
)


@log_execution_time(logger=LOGGER)
def day04_part1(
    input_str: str = "..@@.@@@@.\n@@@.@.@.@@\n@@@@@.@.@@\n@.@@@@..@.\n@@.@@@@.@@"
    "\n.@@@@@@@.@\n.@.@.@.@@@\n@.@@@.@@@@\n.@@@@@@@@.\n@.@.@@@.@.",
) -> int:
    rows = input_str.splitlines()
    # assiming all are identical, which I think they must be
    row_len = len(rows[0])
    accessible = []
    # first I am going to nested for loop the ... out of this problem, later I
    # want to try come up with a solution that does not rely on looping over each
    # individual cell in the grid
    for row_number in range(len(rows)):
        current_row = rows[row_number]
        prev_row = rows[row_number - 1] if row_number > 0 else None
        next_row = rows[row_number + 1] if row_number + 1 < len(rows) else None
        for col_number in range(row_len):
            if current_row[col_number] != "@":
                continue
            adjacent_idxs = [
                col_number + i for i in [-1, 0, 1] if 0 <= col_number + i < row_len
            ]
            # ensuring I only add the values if not at the edge of a row
            values = [current_row[col_number - 1]] if col_number > 0 else []
            values += [current_row[col_number + 1]] if col_number + 1 < row_len else []
            if prev_row:
                values += [
                    val for val in prev_row[adjacent_idxs[0] : adjacent_idxs[-1] + 1]
                ]
            if next_row:
                values += [
                    val for val in next_row[adjacent_idxs[0] : adjacent_idxs[-1] + 1]
                ]
            count = values.count("@")
            if count < 4:
                accessible.append((row_number, col_number))
    return len(accessible)


@log_execution_time(logger=LOGGER)
def day00_part2(
    input_str: str = "..@@.@@@@.\n@@@.@.@.@@\n@@@@@.@.@@\n@.@@@@..@.\n@@.@@@@.@@"
    "\n.@@@@@@@.@\n.@.@.@.@@@\n@.@@@.@@@@\n.@@@@@@@@.\n@.@.@@@.@.",
):
    rows = input_str.splitlines()
    row_len = len(rows[0])
    accessible = []
    changes_last_iter = row_len * len(rows)
    # I hate that I have used a while loop here, I am going to revisit this problem
    # and find a way to do it without the nested looping approach, but I wanted
    # to solve it quickly this time instead of spending ages on the problem.
    # I will revisit this later with the plan not to brute force the answer ...
    # to be safe I will add a break condition to prevent infinite loop at least
    max_iterations = 10000
    iteration = 0
    while changes_last_iter != 0 and iteration < max_iterations:
        iteration += 1
        changes_this_iter = 0
        for row_number in range(len(rows)):
            current_row = rows[row_number]
            prev_row = rows[row_number - 1] if row_number > 0 else None
            next_row = rows[row_number + 1] if row_number + 1 < len(rows) else None
            for col_number in range(row_len):
                if current_row[col_number] != "@":
                    continue
                adjacent_idxs = [
                    col_number + i for i in [-1, 0, 1] if 0 <= col_number + i < row_len
                ]
                values = [current_row[col_number - 1]] if col_number > 0 else []
                values += (
                    [current_row[col_number + 1]] if col_number + 1 < row_len else []
                )
                if prev_row:
                    values += [
                        val
                        for val in prev_row[adjacent_idxs[0] : adjacent_idxs[-1] + 1]
                    ]
                if next_row:
                    values += [
                        val
                        for val in next_row[adjacent_idxs[0] : adjacent_idxs[-1] + 1]
                    ]
                count = values.count("@")
                if count < 4:
                    # I made the mistake of removing the rolls of paper at this stage at first,
                    # resulting in far too many being removed as it freed them up mid iteration
                    accessible.append((row_number, col_number))
                    changes_this_iter += 1
        changes_last_iter = changes_this_iter
        # making sure to only remove indexes added this iteration but keep the full
        # list for later length calculation
        for accessed in accessible[-changes_this_iter:]:
            row_number, col_number = accessed
            current_row = rows[row_number]
            rows[row_number] = (
                current_row[:col_number] + "." + current_row[col_number + 1 :]
            )
    return len(accessible)


if __name__ == "__main__":
    expected_solution = 13
    got_solution = day04_part1()
    if expected_solution != got_solution:
        LOGGER.error(
            f"Problem with solution to part 1! Did not get the expected answer of {expected_solution} for the provided worked example. Instead got: {got_solution}"
        )

    input_str = read_day_input(
        day=4, folder=Path(__file__).resolve().parent.parent / "inputs"
    )
    part1_solution: int = day04_part1(input_str)
    LOGGER.info(f"Part 1 solution: {part1_solution}")

    expected_solution = 43
    got_solution = day00_part2()
    if expected_solution != got_solution:
        LOGGER.error(
            f"Problem with solution to part 2! Did not get the expected answer of {expected_solution} for the provided worked example. Instead got: {got_solution}"
        )

    part2_solution: int = day00_part2(input_str)
    LOGGER.info(f"Part 2 solution: {part2_solution}")
