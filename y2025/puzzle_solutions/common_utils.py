#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
File: common_utils.py
Project: advent-of-code
File Created: Tuesday, 2nd December 2025 9:49:46 pm
Author: tdarnell (tdarnell@users.noreply.github.com)
-----
Last Modified: Saturday, 6th December 2025 2:43:53 pm
Modified By: tdarnell (tdarnell@users.noreply.github.com>)
-----
HISTORY:
Date      	By	Comments
----------	---	---------------------------------------------------------
"""

import logging
from pathlib import Path
import time


def set_up_logger(
    day: int, folder: Path | None = None, level=logging.INFO
) -> logging.Logger:
    """
    Set up a logger for the given day with some standardised handlers.

    Parameters
    ----------
    day : int
        The day number.
    folder : Path | None, optional
        The folder to save the log file in. If None, defaults to ./logs
    level : _type_, optional
        The logging level, by default logging.INFO

    Returns
    -------
    logging.Logger
        The configured logger.
    """
    LOGGER: logging.Logger = logging.getLogger(f"day{day:02d}")
    LOGGER.setLevel(level)
    # Create a file handler
    file_handler = logging.FileHandler(
        Path(folder) / f"day{day:02d}.log"
        if folder
        else Path(".") / "logs" / f"day{day:02d}.log"
    )
    file_handler.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    # Create a logging format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    # Add the handlers to the logger
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(stream_handler)
    return LOGGER


def read_day_input(day: int, folder: Path | None = None) -> str:
    """
    Read the input file and return the contents as a string.

    Parameters
    ----------
    input_file : Path
        The path to the input file.

    Returns
    -------
    str
        The contents of the input file as a string, this is not split into lines.
    """
    file_path = (
        Path(folder) / f"day{day:02d}.txt"
        if folder
        else Path(".") / "inputs" / f"day{day:02d}.txt"
    )
    input_file: Path = Path(file_path)
    if not isinstance(input_file, Path):
        raise AttributeError(
            "Expected an input_file of type Path, got type ", type(input_file)
        )
    if not input_file.exists():
        raise FileNotFoundError(f"Input file {input_file} not found.")
    with open(input_file, "r") as f:
        return f.read()  # .strip()


def log_execution_time(func=None, *, logger=None):
    """
    Decorator that logs the execution time of a function.

    Parameters
    ----------
    func : callable, optional
        The function to wrap.
    logger : logging.Logger, optional
        The logger to use. If not provided, the root logger will be used.

    Returns
    -------
    callable
        The wrapped function.
    """

    if func is None:
        return lambda f: log_execution_time(f, logger=logger)

    if logger is None:
        logger = logging.getLogger()

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(
            f"Function {func.__name__} executed in {end_time - start_time:.4f} seconds"
        )
        return result

    return wrapper
