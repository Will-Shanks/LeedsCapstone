#!/usr/bin/env python3
"""Find company names in 1 col pages"""

import logging


def get_titles(lines):
    """Prints out company names found in given .day files

    Args:
        lines (Generator[str, None, None]): generator that produces the manual
        line by line

    Returns:
        list[str]: list of company names found

    Note: if a name miss is detected "MISSED COMPANY NAME" is added to the
        returned name list
    """
    # list of company names to return
    titles = []
    # default company name (if name is missed)
    lastline = "MISSED COMPANY NAME"

    # iter over manual line by line
    for line in lines():
        # companies have a history section first so if we found it then we've
        # gone past a company name
        if line.startswith('History'):
            titles.append(lastline)
            lastline = "MISSED COMPANY NAME"
        else:
            # if line is not just punctuation and numbers and is all uppercase
            # then probably a company name

            # check if all punctuation and numbers
            table_row = line.replace(".", "").replace(" ", "").isdigit()
            if line.isupper() and not table_row:
                logging.debug("Found potential company name: %s", line)
                lastline = line
    return titles
