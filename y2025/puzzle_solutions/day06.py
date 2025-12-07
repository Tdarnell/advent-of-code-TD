#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
File: day06.py
Project: advent-of-code
File Created: Saturday, 6th December 2025 12:34:12 pm
Author: tdarnell (tdarnell@users.noreply.github.com)
-----
Last Modified: Saturday, 6th December 2025 2:43:10 pm
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
    level=logging.INFO,
)


@log_execution_time(logger=LOGGER)
def day06_part1(
    input_str="123 328  51 64 \n 45 64  387 23 \n  6 98  215 314\n*   +   *   +  ",
) -> int:
    """
    Cephalopod math worksheets consist of a horizontal list of problems. Each problem has a group of numbers
    arranged vertically, with the operation (+ or *) indicated at the bottom of the problem. Problems are separated
    by a column of only spaces. The alignment of numbers within each problem can be ignored.

    For example:

        123 328  51 64
         45 64  387 23
          6 98  215 314
        *   +   *   +

    This worksheet contains four problems:

        - 123 * 45 * 6 = 33210
        - 328 + 64 + 98 = 490
        - 51 * 387 * 215 = 4243455
        - 64 + 23 + 314 = 401

    The grand total is the sum of all problem answers: 4277556.

    Parameters
    ----------
    input_str : str, optional
        The cephalopod math worksheet, by default "123 328  51 64 \n 45 64  387 23 \n  6 98  215 314\n*   +   *   +  "

    Returns
    -------
    int
        The grand total found by adding together all answers.
    """

    rows = input_str.splitlines()
    operators = rows[-1].replace(" ", "")
    # match numbers split by whitespace
    rows_num = [re.findall(r"\d+", row) for row in rows[:-1]]
    answer = 0
    for col in range(len(operators)):
        digits = [int(rows_num[row][col]) for row in range(len(rows_num))]
        if operators[col] == "+":
            col_result = sum(digits)
        elif operators[col] == "*":
            col_result = 1
            for d in digits:
                col_result *= d
        answer += col_result
    return answer


@log_execution_time(logger=LOGGER)
def day06_part2(
    input_str="123 328  51 64 \n 45 64  387 23 \n  6 98  215 314\n*   +   *   +  ",
) -> int:
    """
    Cephalopod math is written right-to-left in columns. Each number is given in its own column,
    with the most significant digit at the top and the least significant digit at the bottom.
    Problems are separated by a column consisting only of spaces, and the symbol at the bottom
    of the problem is the operator to use.

    For example, given the worksheet:

        123 328  51 64
         45 64  387 23
          6 98  215 314
        *   +   *   +

    Reading right-to-left, the problems are:

        - Rightmost: 4 + 431 + 623 = 1058
        - Second from right: 175 * 581 * 32 = 3253600
        - Third from right: 8 + 248 + 369 = 625
        - Leftmost: 356 * 24 * 1 = 8544

    The grand total is the sum of all problem answers: 3263827.

    Parameters
    ----------
    input_str : str, optional
        The cephalopod math worksheet, by default "123 328  51 64 \n 45 64  387 23 \n  6 98  215 314\n*   +   *   +  "

    Returns
    -------
    int
        The grand total found by adding together all answers.
    """
    rows = input_str.splitlines()
    # The space is being trimmed off the end of the operators line somehow ...
    # Found it in my common_utils I always stripped the input, poor assumption
    operators = rows.pop(-1)
    # I realised I can just iterate over the operators row and use
    # that to determine my columns ...
    current_operator = operators[0]
    current_digits = []
    answer = 0
    for idx, operator in enumerate(operators):
        if operator != " " and idx != 0:
            if current_operator == "+":
                col_result = sum(current_digits)
            elif current_operator == "*":
                col_result = 1
                for d in current_digits:
                    col_result *= d
            answer += col_result
            LOGGER.debug(
                f"Processed column with operator '{current_operator}': {current_digits} => {col_result}"
            )
            current_operator = operator
            current_digits: list[int] = []
        digit = ""
        for row_idx, row in enumerate(rows):
            digit += row[idx]
        if digit.strip() == "":
            continue
        digit_int = int(digit.strip())
        current_digits.append(digit_int)
    # process last column
    if current_operator == "+":
        col_result: int = sum(current_digits)
    elif current_operator == "*":
        col_result = 1
        for d in current_digits:
            col_result *= d
    LOGGER.debug(
        f"Finally processed column with operator '{current_operator}': {current_digits} => {col_result}"
    )
    answer += col_result
    return answer


if __name__ == "__main__":
    expected_solution = 4277556
    got_solution = day06_part1()
    if expected_solution != got_solution:
        LOGGER.error(
            f"Problem with solution to part 1! Did not get the expected answer of {expected_solution} for the provided worked example. Instead got: {got_solution}"
        )

    input_str = read_day_input(
        day=6, folder=Path(__file__).resolve().parent.parent / "inputs"
    )
    part1_solution: int = day06_part1(input_str)
    LOGGER.info(f"Part 1 solution: {part1_solution}")

    expected_solution = 3263827
    got_solution = day06_part2()
    if expected_solution != got_solution:
        LOGGER.error(
            f"Problem with solution to part 2! Did not get the expected answer of {expected_solution} for the provided worked example. Instead got: {got_solution}"
        )

    part2_solution: int = day06_part2(input_str)
    LOGGER.info(f"Part 2 solution: {part2_solution}")
