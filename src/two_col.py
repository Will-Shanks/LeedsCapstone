#!/usr/bin/env python3
"""Find company names in 2 col pages"""
import logging


def get_titles(lines):
    """Returns company names found in lines
    Args:
        lines Iterator(str): something iterable that produces the manual
        line by line
    Returns:
        [str]: list of company names found
    """
    titles = []
    for line in lines():
        # split line into words
        lastword = line.split()
        # check line contains at least a word
        if not lastword:
            continue
        lastword = lastword[-1]
        if ("incorporated" in line.lower()
                or "Controlled" in line
                or "Organized" in line
                or lastword.startswith("In")):
            logging.debug("Found potential company name in line %s", line)
            t = " ".join((word for word in line.split()
                          if word.isupper()))
            if t != '':
                logging.info("Found company name: %s", t)
                titles.append(t)
    return titles
