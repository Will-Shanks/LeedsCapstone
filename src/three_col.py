#!/usr/bin/env python3
"""Get company names from .day 3 col files"""
import logging

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
    # list to contain company titles
    titles = []
    # iter through all lines
    for line in dayToDF.iter_df(dayToDF.get_df(fn)):
        # If line contains a key word, then is a company name
        if line.split(' ', 1)[0].isupper() and ("Inco" in line or "In-" in line
                                                or "Manufactures" in line
                                                or "Established" in line):
            logging.debug("Found company name line: %s", line)
            # grab the full caps words, rest are start of company info
            t = ' '.join((x for x in line.split() if x.isupper()))
            logging.debug("Extracted company name from line: %s", t)
            titles.append(t)
    return titles


if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) < 2:
        logging.error("Usage: %s FILE, where FILE is a .day filepath",
                      __file__)
        sys.exit(1)
    for filename in sys.argv[1:]:
        print("{}".format(get_titles(filename)))
    sys.exit()
