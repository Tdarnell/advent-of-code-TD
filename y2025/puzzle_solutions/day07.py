#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
File: day07.py
Project: advent-of-code
File Created: Sunday, 7th December 2025 7:34:55 pm
Author: tdarnell (tdarnell@users.noreply.github.com)
-----
Last Modified: Sunday, 7th December 2025 8:56:11 pm
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
def day07_part1(
    input_str=".......S.......\n...............\n.......^.......\n...............\n......^.^......\n...............\n.....^.^.^.....\n...............\n....^.^...^....\n...............\n...^.^...^.^...\n...............\n..^...^.....^..\n...............\n.^.^.^.^.^...^.\n...............\n",
) -> int:
    """
    To repair the teleporter, I need to analyze the beam-splitting properties of the tachyon manifold.
    The worksheet represents a grid where a tachyon beam starts at 'S' and travels downward. Each '^' is a splitter:
    when the beam hits a splitter, it splits into two beams, one going left and one going right. This function
    calculates the total number of times the beam is split as it traverses the manifold. I.e. the number of
    splitters hit in total.

    I overthought this problem at first and started calculating the total count of beams produced by the splitters.

    Parameters
    ----------
    input_str : str, optional
        The tachyon manifold grid, by default the provided example.

    Returns
    -------
    int
        The total number of times the beam is split.
    """
    rows = input_str.splitlines()
    s_index = rows[0].index("S") if "S" in rows[0] else None
    if not s_index:
        LOGGER.error("No starting point 'S' found in the input!")
        raise ValueError("No starting point 'S' found in the input!")
    beam_indexes = {s_index}
    # I overthought the problem and calculated the number of times the beam was split instead of the number of manifolds hit by the beam, kept it in incase I need it for part 2
    split_count = 0
    manifolds_hit = 0
    for row in rows:
        manifolds = [j for j, val in enumerate(row) if val == "^"]
        split_indexes = []
        for m in manifolds:
            if m in beam_indexes:
                manifolds_hit += 1
                beam_indexes.remove(m)
                if m >= 1:
                    split_indexes.append(m - 1)
                if m < len(row) - 1:
                    split_indexes.append(m + 1)

        split_indexes = set(split_indexes)
        split_indexes = split_indexes - beam_indexes
        beam_indexes.update(split_indexes)
        LOGGER.debug(
            "".join(["|" if j in beam_indexes else row[j] for j in range(len(row))])
        )
        split_count += len(split_indexes)
    return manifolds_hit


@log_execution_time(logger=LOGGER)
def day07_part2(
    input_str=".......S.......\n...............\n.......^.......\n...............\n......^.^......\n...............\n.....^.^.^.....\n...............\n....^.^...^....\n...............\n...^.^...^.^...\n...............\n..^...^.....^..\n...............\n.^.^.^.^.^...^.\n...............\n",
) -> int:
    """
    In part two, the manifold is quantum: a single tachyon particle takes both the left and right path at each splitter,
    splitting time itself into multiple timelines. Each time I encounter a splitter, the number of timelines doubles
    for that particle's possible journeys. This function calculates the total number of timelines active after a single particle
    complete all possible journeys through the manifold.

    I started with an approach where I added +2 for each splitter hit, but realised that this was too simplistic as it does
    not solve the pascals triangle problem presented.

    Parameters
    ----------
    input_str : str, optional
        The quantum tachyon manifold grid, by default the provided example.

    Returns
    -------
    int
        The total number of timelines active after all possible journeys.
    """
    rows = input_str.splitlines()
    s_index = rows[0].index("S")
    beam_indexes = {s_index}
    timelines = [0] * len(rows[0])
    timelines[s_index] = 1
    for i, row in enumerate(rows):
        manifolds = [j for j, val in enumerate(row) if val == "^"]
        split_indexes = []
        for m in manifolds:
            if m in beam_indexes:
                beam_indexes.remove(m)
                if m >= 1:
                    split_indexes.append(m - 1)
                    timelines[m - 1] += timelines[m]
                if m < len(row) - 1:
                    timelines[m + 1] += timelines[m]
                    split_indexes.append(m + 1)
                timelines[m] = 0
        split_indexes = set(split_indexes)
        split_indexes = split_indexes - beam_indexes
        beam_indexes.update(split_indexes)
    return sum(timelines)


if __name__ == "__main__":
    expected_solution = 21
    got_solution = day07_part1()
    if expected_solution != got_solution:
        LOGGER.error(
            f"Problem with solution to part 1! Did not get the expected answer of {expected_solution} for the provided worked example. Instead got: {got_solution}"
        )

    input_str = read_day_input(
        day=7, folder=Path(__file__).resolve().parent.parent / "inputs"
    )
    part1_solution: int = day07_part1(input_str)
    LOGGER.info(f"Part 1 solution: {part1_solution}")

    expected_solution = 40
    got_solution = day07_part2()
    if expected_solution != got_solution:
        LOGGER.error(
            f"Problem with solution to part 2! Did not get the expected answer of {expected_solution} for the provided worked example. Instead got: {got_solution}"
        )

    part2_solution: int = day07_part2(input_str)
    LOGGER.info(f"Part 2 solution: {part2_solution}")
