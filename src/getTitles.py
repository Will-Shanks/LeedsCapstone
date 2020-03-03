#!/usr/bin/env python3
"""prints company names in text generated from 1 col pages

Example:
    $ ./getTitles.py /path/to/.day [...]
"""

import logging
import sys

import dayToDF
import nav

def getTitles(lines):
    """Prints out company names found in given .day files

    Args:
        lines (Generator[str, None, None]): generator that produces the manual line by line

    Returns:
        list[str]: list of company names found
        Note: if a name miss is detected "MISSED COMPANY NAME" is added to the name list
    """
    titles = []
    # iter over given files
    lastline = "MISSED COMPANY NAME"
    # iter over lines in file
    for line in lines():
        # companies have a history section first
        if line.startswith('History'):
            titles.append(lastline)
            lastline = "MISSED COMPANY NAME"
            continue
        # check if line might be a company name
        table_row = line.replace(".", "").replace(" ", "").isdigit()
        if line.isupper() and not table_row:
            lastline = line
    return titles


if __name__ == '__main__':
    print("started program")
    if len(sys.argv) < 2:
        logging.error("Usage: %s YEAR", __file__) #DAYFILE [DAYFILE [...]]", __file__)
        sys.exit(1)
    sys.exit(getTitles(sys.argv[1]))
