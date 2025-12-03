#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
File: day01.py
Project: advent-of-code
File Created: Tuesday, 2nd December 2025 9:49:33 pm
Author: tdarnell (tdarnell@users.noreply.github.com)
-----
Last Modified: Wednesday, 3rd December 2025 11:04:54 pm
Modified By: tdarnell (tdarnell@users.noreply.github.com>)
-----
HISTORY:
Date      	By	Comments
----------	---	---------------------------------------------------------

03-12-2025	TD	Slow start this year, I got stuck on part 2 for a while and took
a break between parts, but was really pleased with my solution in the end.
I went down a bit of a rabbit hole thinking I could calculate the number of 0
crossings without a seperate if statement for the L and R movements but realised
that was not possible in the end. My approach was attempting to use
(end // 100 - start // 100) then add some edge cases in seperately, but it was
a flawed approach.

02-12-2025	TD  This year I would like to focus on making unit tests for my code
before I submit my answer

I need to calculate the number of times the cumulative sum of dial rotations
equals 0, where it starts at 50 and a turn to the right "R" increases the value
and turning to the left "L" decreases the value, passing 99 or 0 circles back.

My initial thought was can I use regex to replace all "L" with "-" and
all "R" with "", then sum the result however that only gives me the final value

I of course could do a for loop ... and I may well do that first just as a proof
that I have understood the problem, however it is computationally slow! So I
absolutely do want to vectorize the problem ... maybe a form of np cumulative sum
"""

import logging
from pathlib import Path

import numpy as np

try:
    from .common_utils import log_execution_time, set_up_logger, read_day_input
except (ImportError, ValueError):
    from common_utils import log_execution_time, set_up_logger, read_day_input

LOGGER: logging.Logger = set_up_logger(
    day=int(Path(__file__).stem[3:]),
    folder=str(Path(__file__).resolve().parent.parent / "logs"),
)


@log_execution_time(logger=LOGGER)
def day01_part1_for_loop_method(
    input_str: str = "L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82",
) -> int:
    """
    My first sloppy attempt at solving the problem, I know that I can improve on
    this one but will write it anyway so that I can prove I have understood the
    question.

    Parameters
    ----------
    input_str : str, optional
        The input puzzle string, by default "L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82"

    Returns
    -------
    int
        The number of times the cumulative sum equals 0.
    """
    start_position = 50
    moves_str = input_str.replace("L", "-").replace("R", "")
    moves_lines: list[str] = moves_str.splitlines()
    rotations: list[int] = [int(m) for m in moves_lines]
    current_position = start_position
    zero_count = 0
    for step_index, rotation in enumerate(rotations):
        # Calculate new position, wrapping past 100 or 0
        current_position = (current_position + rotation) % 100
        if current_position == 0:
            zero_count += 1
        LOGGER.debug(
            "Step %d: Turn %s, New Value: %d",
            step_index + 1,
            rotation,
            current_position,
        )
    return zero_count


@log_execution_time(logger=LOGGER)
def day01_part1_vectorized(
    input_str: str = "L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82",
) -> int:
    """
    A vectorized solution to the problem using numpy arrays.

    Parameters
    ----------
    input_str : str, optional
        The input puzzle string, by default "L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82"

    Returns
    -------
    int
        The number of times the cumulative sum equals 0.
    """
    start_position = 50
    if not input_str:
        return 0
    moves_str = input_str.replace("L", "-").replace("R", "")
    rotations = np.fromstring(moves_str, dtype=np.int16, sep="\n")
    if rotations.size == 0:
        return 0
    # Use a wider dtype for the cumulative sum to avoid overflow, then reduce modulo 100
    positions = (start_position + np.cumsum(rotations, dtype=np.int32)) % 100
    zero_count = int(np.count_nonzero(positions == 0))

    LOGGER.debug("Vectorized: %d zeros", zero_count)
    return zero_count


@log_execution_time(logger=LOGGER)
def day01_part2_for_loop_method(
    input_str: str = "L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82",
) -> int:
    """
    Solution to part 2 of the puzzle, counting the number of times the dial
    passes 0. I am not sure I can vectorize this one easily so will come back to it.

    Parameters
    ----------
    input_str : str, optional
        Puzzle input, by default "L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82"

    Returns
    -------
    int
        The number of times the dial passes 0.
    """
    moves_str = input_str.replace("L", "-").replace("R", "")
    moves_lines: list[str] = moves_str.splitlines()
    rotations: list[int] = [int(m) for m in moves_lines]
    current_position = 50
    zero_count = 0
    for step_index, rotation in enumerate(rotations):
        if rotation == 0:
            continue

        start = current_position
        end = start + rotation

        if rotation < 0 and abs(rotation) >= start:
            zero_count += abs(end) // 100 + (start != 0)
        else:
            zero_count += end // 100

        current_position = end % 100

        LOGGER.debug(
            "Step %d: Turn %s, New Value: %d, Passed Zero: %d",
            step_index + 1,
            rotation,
            current_position,
            zero_count,
        )
    return zero_count


if __name__ == "__main__":
    expected_solution: int = day01_part1_for_loop_method()
    if expected_solution != 3:
        LOGGER.error(
            f"Problem with solution to part 1! Did not get the expected answer of 3 for the provided worked example. Instead got: {expected_solution}"
        )

    input_str = read_day_input(
        day=1, folder=Path(__file__).resolve().parent.parent / "inputs"
    )
    part1_solution: int = day01_part1_for_loop_method(input_str)
    LOGGER.info(f"Part 1 solution: {part1_solution}")

    expected_solution: int = day01_part1_vectorized()
    if expected_solution != 3:
        LOGGER.error(
            f"Problem with solution to part 1! Did not get the expected answer of 3 for the provided worked example. Instead got: {expected_solution}"
        )

    input_str = read_day_input(
        day=1, folder=Path(__file__).resolve().parent.parent / "inputs"
    )
    part1_solution: int = day01_part1_vectorized(input_str)
    LOGGER.info(f"Part 1 solution: {part1_solution}")

    # The runtime of the for loop approach is 0.0018 seconds whereas the numpy
    # approach executes in 0.0003 seconds
    # Interestingly the test function takes 0.0001 seconds longer to initialise
    # in the numpy approach, likely due to the overhead of initialising C type
    # arrays vs using pure python

    expected_solution = day01_part2_for_loop_method()
    if expected_solution != 6:
        LOGGER.error(
            f"Problem with solution to part 2! Did not get the expected answer of 6 for the provided worked example. Instead got: {expected_solution}"
        )

    part2_solution: int = day01_part2_for_loop_method(input_str)
    LOGGER.info(f"Part 2 solution: {part2_solution}")

    # The runetime for part 2 is fairly significant, 0.0057 seconds
    # However I struggle to see how this one can be vectorized with the logic involved
