#!/usr/bin/env python3
"""prints company names in text generated from 1 col pages"""

import logging
import sys

import dayToDF


def main(args):
    """
    Prints out company names found in given .day files
    input: list of filepaths for .day files
    output: None
    """
    # iter over given files
    for fn in args:
        lastline = "MISSED COMPANY NAME"
        # iter over lines in file
        for line in dayToDF.iter_df(dayToDF.get_df(fn)):
            # companies have a history section first
            if line.startswith('History'):
                print("'{}'".format(lastline), end=' ')
                lastline = "MISSED COMPANY NAME"
                continue
            # check if line might be a company name
            table_row = line.replace(".", "").replace(" ", "").isdigit()
            if line.isupper() and not table_row:
                lastline = line
        print("")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: %s DAYFILE [DAYFILE [...]]", __file__)
        sys.exit(1)
    sys.exit(main(sys.argv[1:]))
