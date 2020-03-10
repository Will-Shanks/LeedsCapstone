#!/usr/bin/env python3
"""Get company names from .day 3 col files"""
import logging
import re

import dayToDF


def get_titles(fn):
    """Prints out company names found in given .day files
        Args:
            filename (str): filepath to the .day file
        Returns:
            list[str]: list of company names found
        Note:
            Only works on 3col pages
    """
    titles = []
    for line in dayToDF.iter_df(dayToDF.get_df(fn)):
        if line.split(' ', 1)[0].isupper():
            if ("Inco" in line or "In-" in line or "Manufactures" in line
                    or "Established" in line):
                *_, element = (x.strip() for x in
                               re.findall(r"\b[A-Z\s]+\b", line) if x.strip())
                titles.append(element)
    return titles


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        logging.error("Usage: %s FILE, where FILE is a .day filepath",
                      __file__)
        sys.exit(1)
    for filename in sys.argv[1:]:
        print("{}".format(get_titles(filename)))
    sys.exit()
