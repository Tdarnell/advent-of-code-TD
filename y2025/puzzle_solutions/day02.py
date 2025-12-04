#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
File: day02.py
Project: advent-of-code
File Created: Thursday, 4th December 2025 9:01:43 pm
Author: tdarnell (tdarnell@users.noreply.github.com)
-----
Last Modified: Thursday, 4th December 2025 10:50:21 pm
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
def day02_part1(
    input_str: str = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124",
) -> int:
    input_ranges = input_str.split(",")
    total = 0
    for i, rng in enumerate(input_ranges):
        try:
            start, end = rng.split("-")
            start, end = int(start), int(end)
            if start > end:
                LOGGER.warning("Start greater than end in range %d: %s", i + 1, rng)
                continue
        except ValueError:
            LOGGER.error("Invalid range format at index %d: %s", i + 1, rng)
            continue

        for n in range(start, end + 1):
            ns = str(n)
            if len(ns) % 2 == 0 and ns[: len(ns) // 2] == ns[len(ns) // 2 :]:
                LOGGER.debug("Found a match on range %d: %s", i + 1, ns)
                total += n
    return total


@log_execution_time(logger=LOGGER)
def day02_part2(
    input_str: str = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124",
):
    input_ranges = input_str.split(",")
    total = 0
    for i, rng in enumerate(input_ranges):
        try:
            start, end = rng.split("-")
            start, end = int(start), int(end)
            if start > end:
                LOGGER.warning("Start greater than end in range %d: %s", i + 1, rng)
                continue
        except ValueError:
            LOGGER.error("Invalid range format at index %d: %s", i + 1, rng)
            continue

        # I have left my first string based approach in, but I realised after playing
        # around in a jupyter notebook that repeating patterns will always have
        # a multiple starting in 1 and ending 1
        # for n in range(start, end + 1):
        #     ns = str(n)
        #     if ns == ns[0] * len(ns):
        #         LOGGER.debug(
        #             "Found a match on range %d: %s (all identical digits)", i + 1, ns
        #         )
        #         total += n
        #         continue
        #     for pattern_len in range(2, (len(ns) // 2) + 1):
        #         chunks = tuple(
        #             ns[i : i + pattern_len] for i in range(0, len(ns), pattern_len)
        #         )
        #         if all(chunk == chunks[0] for chunk in chunks):
        #             LOGGER.debug(
        #                 "Found a match on range %d: %s with pattern length %d",
        #                 i + 1,
        #                 ns,
        #                 pattern_len,
        #             )
        #             total += n
        #             break

        # I experimented with dividing the numbers by their repeating parts, and
        # discovered that the result was always a number like 101, 1001, 1001001 etc
        # and so I looked into this and came up with a solution
        # For each possible block length k (from 1 to half the number of digits):
        # If the total length is divisible by k, compute s = (10^{k*n} - 1) // (10^k - 1)
        # If n % s == 0, then n is a repeating pattern.
        for n in range(start, end + 1):
            ns_len = len(str(n))
            possible_blocks = [
                k for k in range(1, (ns_len // 2) + 1) if (ns_len % k == 0)
            ]
            for block in possible_blocks:
                block_divisor = (10**ns_len - 1) // (10**block - 1)
                if n % block_divisor == 0:
                    total += n
                    break
    return total


if __name__ == "__main__":
    expected_solution = 1227775554
    got_solution = day02_part1()
    if expected_solution != got_solution:
        LOGGER.error(
            f"Problem with solution to part 1! Did not get the expected answer of {expected_solution} for the provided worked example. Instead got: {got_solution}"
        )

    input_str = read_day_input(
        day=2, folder=Path(__file__).resolve().parent.parent / "inputs"
    )
    part1_solution: int = day02_part1(input_str)
    LOGGER.info(f"Part 1 solution: {part1_solution}")

    expected_solution = 4174379265
    got_solution = day02_part2()
    if expected_solution != got_solution:
        LOGGER.error(
            f"Problem with solution to part 2! Did not get the expected answer of {expected_solution} for the provided worked example. Instead got: {got_solution}"
        )

    part2_solution: int = day02_part2(input_str)
    LOGGER.info(f"Part 2 solution: {part2_solution}")
