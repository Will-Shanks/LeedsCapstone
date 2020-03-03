#!/usr/bin/env python3
import glob

def pages(year, brightness='70', basepath='/scratch/summit/diga9728/Moodys/Industrials/'):
    """Iterates over all files in a year, for a certain brightness

    Args:
        year: (str): year of manuals to iterate through
        TODO

    Yields:
        str: filepath of next page in manual
    """

    dirs = sorted(glob.glob(basepath+'OCRrun'+year+'/'+'[0-9][0-9][0-9]/'))
    for d in dirs:
        #OCRoutputIndustrial<year><fiche>-<image#><brightness>.day
        files = sorted(glob.glob(d+'OCRoutputIndustrial'+year+'[0-9][0-9][0-9][6-9]'+'-'+'[0-9][0-9][0-9][0-9]'+brightness+'.day'))
        for f in files:
            yield f


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Error: usage: {} year".format(__file__))
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
