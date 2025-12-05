#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
File: day03.py
Project: advent-of-code
File Created: Friday, 5th December 2025 9:23:08 pm
Author: tdarnell (tdarnell@users.noreply.github.com)
-----
Last Modified: Friday, 5th December 2025 10:31:16 pm
Modified By: tdarnell (tdarnell@users.noreply.github.com>)
-----
HISTORY:
Date      	By	Comments
----------	---	---------------------------------------------------------
"""

import logging
import math
from pathlib import Path


try:
    from .common_utils import log_execution_time, set_up_logger, read_day_input
except (ImportError, ValueError):
    from common_utils import log_execution_time, set_up_logger, read_day_input

LOGGER: logging.Logger = set_up_logger(
    day=int(Path(__file__).stem[3:]),
    folder=str(Path(__file__).resolve().parent.parent / "logs"),
    level=logging.INFO,
)


# I have realised a flaw with this approach after checking my input txt
# the integers are far too large, I will need to use a string based approach
def extract_digits(num: int) -> list[int]:
    if num == 0:
        return [0]
    # Source - https://stackoverflow.com/a
    # Posted by inspectorG4dget, modified by community. See post 'Timeline' for change history
    # Retrieved 2025-12-05, License - CC BY-SA 4.0
    return [(num // (10**i)) % 10 for i in range(math.ceil(math.log(num, 10)), -1, -1)][
        bool(math.log(num, 10) % 1) :
    ]


def find_joltage(digits: list[int], num_maxs=2) -> int:
    """
    Calculates the largest number that can be formed from the digits in linear
    order, by selecting the largest `num_maxs` digits while maintaining
    their relative order.

    Initial implementation hard coded to find 2 maxima
    (as per scratchpad jupyter notebook)

    Parameters
    ----------
    digits : list[int]
        A list of integers representing the digits.
    num_maxs : int, optional
        The number of maximum digits to find, by default 2

    Returns
    -------
    int
        The largest number formed by the selected digits.

    Raises
    ------
    ValueError
        If the input is not a list of integers or is empty.
        Also raised if there are not enough digits to select the maxima from.
    IndexError
        If slice indices go out of range during processing.
    """
    if not digits:
        return 0
    if not isinstance(digits, list):
        raise ValueError("Input to find_joltage must be a list of integers.")
    if not all(isinstance(d, int) for d in digits):
        raise ValueError("All elements in the input list must be integers.")
    output = 0
    current_slice_start = 0
    try:
        for m in range(num_maxs):
            current_slice_end = len(digits) - (num_maxs - (m + 1))
            if current_slice_start >= current_slice_end:
                raise IndexError("Slice indices out of range while finding maxima.")
            slice_digits = digits[current_slice_start:current_slice_end]
            if not slice_digits:
                raise ValueError("No digits left to select maxima from.")
            next_digit = max(slice_digits)
            current_slice_start = (
                slice_digits.index(next_digit) + current_slice_start + 1
            )
            output = output * 10 + next_digit
    except Exception as e:
        LOGGER.error(f"Error in find_joltage: {e}")
        raise
    return output


@log_execution_time(logger=LOGGER)
def day03_part1(
    input_str: str = "987654321111111\n811111111111119\n234234234234278\n818181911112111",
) -> int:
    input_digits = [[int(i) for i in _] for _ in input_str.strip().splitlines()]
    joltage = 0
    for digits_row in input_digits:
        _row_joltage = find_joltage(digits_row)
        joltage += _row_joltage
        LOGGER.debug("Row digits: %s, Row joltage: %d", digits_row, _row_joltage)
    LOGGER.info("Total joltage: %d", joltage)
    return joltage


@log_execution_time(logger=LOGGER)
def day03_part2(
    input_str: str = "987654321111111\n811111111111119\n234234234234278\n818181911112111",
) -> int:
    input_digits = [[int(i) for i in _] for _ in input_str.strip().splitlines()]
    joltage = 0
    for digits_row in input_digits:
        _row_joltage = find_joltage(digits_row, num_maxs=12)
        joltage += _row_joltage
        LOGGER.debug("Row digits: %s, Row joltage: %d", digits_row, _row_joltage)
    LOGGER.info("Total joltage: %d", joltage)
    return joltage


if __name__ == "__main__":
    input_str = read_day_input(
        day=3, folder=Path(__file__).resolve().parent.parent / "inputs"
    )

    part1_solution: int = day03_part1(input_str)
    LOGGER.info(f"Part 1 solution: {part1_solution}")

    part2_solution: int = day03_part2(input_str)
    LOGGER.info(f"Part 2 solution: {part2_solution}")
