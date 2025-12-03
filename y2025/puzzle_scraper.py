#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
File: puzzle_scraper.py
Project: Advent of Code
File Created: Tuesday, 2nd December 2025 8:56:45 pm
Author: tdarnell (tdarnell@users.noreply.github.com)
-----
Last Modified: Tuesday, 2nd December 2025 9:04:52 pm
Modified By: tdarnell (tdarnell@users.noreply.github.com>)
-----
HISTORY:
Date      	By	Comments
----------	---	---------------------------------------------------------
"""

from http.cookiejar import CookieJar
import os
import requests
from pathlib import Path
import browser_cookie3
import datetime as dt
from dotenv import load_dotenv
import logging

# This script will scrape the puzzle input from the Advent of Code website
# and save it to a file in the inputs folder.
# It will also save a HTML copy of the puzzle page to the inputs folder.

# Load the configuration from the .env file
load_dotenv()
COOKIE_FILE_PATH = Path(os.getenv("COOKIE_FILE_PATH"))
if not COOKIE_FILE_PATH.exists():
    raise FileNotFoundError(f"Cookie file {COOKIE_FILE_PATH} does not exist.")

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
# Create a file handler
file_handler = logging.FileHandler("puzzle_scraper.log")
file_handler.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
# Create a logging format
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
# Add the handlers to the logger
LOGGER.addHandler(file_handler)
LOGGER.addHandler(stream_handler)


class PuzzleScraper:
    def __init__(self, year: int, day: int):
        self.year = year
        self.day = day
        # check that the adventofcode cookies exist in the cookie jar
        self.session_cookie: CookieJar = browser_cookie3.firefox(
            cookie_file=COOKIE_FILE_PATH,
            domain_name=".adventofcode.com",
        )
        if not self.session_cookie:
            raise ValueError(
                f"No cookies found for domain .adventofcode.com in {COOKIE_FILE_PATH}"
            )
        self.puzzle_page_url = f"https://adventofcode.com/{year}/day/{day}"
        self.puzzle_input_url = f"https://adventofcode.com/{year}/day/{day}/input"
        self.puzzle_page_file = Path(f"inputs/day{day:02d}.html")
        self.puzzle_input_file = Path(f"inputs/day{day:02d}.txt")
        if not self.puzzle_page_file.parent.exists():
            self.puzzle_page_file.parent.mkdir(parents=True)
        if not self.puzzle_input_file.parent.exists():
            self.puzzle_input_file.parent.mkdir(parents=True)

    def scrape_puzzle_page(self):
        # Make the request to the puzzle page
        r = requests.get(self.puzzle_page_url, cookies=self.session_cookie)
        if r.status_code != 200:
            LOGGER.error(f"Failed to scrape puzzle page for day {self.day}")
        with open(self.puzzle_page_file, "wb+") as f:
            f.write(r.content)
        return r

    def scrape_puzzle_input(self):
        # Make the request to the puzzle input
        # this requires some trickery as the input is not available until we sign in
        # so we need to use the session cookie from our google chrome browser
        r = requests.get(self.puzzle_input_url, cookies=self.session_cookie)
        if r.status_code != 200:
            LOGGER.error(f"Failed to scrape puzzle input for day {self.day}")
        # Save the puzzle input to a file
        with open(self.puzzle_input_file, "w") as f:
            f.write(r.text)
        # Return the puzzle input
        return r.text


if __name__ == "__main__":
    year = dt.datetime.now().year
    day = dt.datetime.now().day
    # lets also check if all the previous days have been completed
    for d in range(1, day + 1):
        # use asyncio to delay the requests and avoid spamming the server
        scraper = PuzzleScraper(year, d)
        if not scraper.puzzle_input_file.exists():
            LOGGER.info(f"Input file {scraper.puzzle_input_file} does not exist.")
            # Scrape the puzzle
            puzzle_input = scraper.scrape_puzzle_input()
            LOGGER.info(
                f"Scraped puzzle input for day {d}: {str(puzzle_input)[:50]}..."
            )
        else:
            LOGGER.info(f"Input file {scraper.puzzle_input_file} already exists.")
        if not scraper.puzzle_page_file.exists():
            LOGGER.info(f"HTML file {scraper.puzzle_page_file} does not exist.")
            puzzle_page = scraper.scrape_puzzle_page()
            LOGGER.info(
                f"Scraped puzzle page for day {d}: {str(puzzle_page.content)[:50]}..."
            )
        else:
            LOGGER.info(f"HTML file {scraper.puzzle_page_file} already exists.")
