#!/usr/bin/env python3
"""
Parses through a manual from start to finish, finding all the company names

Example:
    ./getTitles.py 1930
"""
import logging
import sys

import dayToDF
import oneCol


def get_titles(year):
    """prints company names for the given year

    Args:
        year (str): year of the manual to be parsed
    """
    # create a day file reader
    dr = dayToDF.DayReader(year)
    # find out how many cols are on first page
    cols = dr.cols()
    # keep going until get to end of manual
    while cols is not None:
        logging.info("Parsing %d column pages, starting with page %s",
                     cols, dr.page())

        # col type multiplexor
        # figure out how to parse based on number of cols
        if cols == 1:
            # get company names for one col pages
            titles = oneCol.get_titles(dr.lines)
            if titles is not None:
                print(titles)
        elif cols == 2:
            # Not implemented yet, so just get iter to next section
            for _ in dr.lines():
                pass
        elif cols == 3:
            # Not implemented yet, so just get iter to next section
            for _ in dr.lines():
                pass
        else:
            # All pages are 1,2, or 3 columns, shouldn't be able to get here
            logging.error("Page %s has %d columns, don't know what to do",
                          dr.page(), cols)
            # iter to next section so can parse rest of manual
            for _ in dr.lines():
                pass

        # In next section, update number of cols on page
        cols = dr.cols()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) < 2:
        logging.error("Usage: %s YEAR", __file__)
        sys.exit(1)
    get_titles(sys.argv[1])
    sys.exit(0)
