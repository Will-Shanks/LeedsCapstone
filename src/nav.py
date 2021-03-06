#!/usr/bin/env python3
"""
Utility functions to simplify navigating the filesystem
"""
import glob
import logging


def pages(year, brightness='70',
          basepath='/scratch/summit/diga9728/Moodys/Industrials/'):
    """Iterates over all files in a year, for a certain brightness

    Note:
        Looks for day files in  <basedir>/OCRrun<year>/[0-9][0-9][0-9]/

    Args:
        year (str): year of manuals to iterate through
        brightness (str, optional): brightness level of day files to use
        basepath (str, optional): filepath to where dirs with day files are

    Yields:
        str: filepath of next page in manual
    """
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(
        "Looking for day files from year %s, at brightness %s, in %s",
        year, brightness, basepath)
    # find all dirs that might contain .day files
    dirs = sorted(glob.glob(basepath + 'OCRrun' + year + '/[0-9][0-9][0-9]/'))
    # iter over these dirs
    for d in dirs:
        # filenames: OCRoutputIndustrial<year><fiche>-<image#><brightness>.day
        # find all filenames in given dir
        files = sorted(glob.glob(d + 'OCRoutputIndustrial' + year + '[0-9]'
                                 '[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]'
                                 + brightness + '.day'))
        # yield page by page
        for f in files:
            yield f


if __name__ == '__main__':
    import sys
    if len(sys.argv) <= 2:
        print("Error: usage: {} year [basepath]".format(__file__))
        sys.exit(1)
    if len(sys.argv) == 3:
        print(list(pages(sys.argv[1], basepath=sys.argv[2])))
    else:
        print(list(pages(sys.argv[1])))
    sys.exit(0)
