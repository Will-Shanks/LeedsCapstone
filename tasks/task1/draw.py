#!/usr/bin/env python3
"""
This script reads in the given file, and generates a graph of the words in it
usage: ./draw.py ocroutput.day
"""

import csv
import logging
import sys

import matplotlib.patches as patches
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)


def main():
    """ Creats a graph of the input file words"""
    logging.debug("openning file %s", sys.argv[1])

    # setup graph
    _, ax = plt.subplots(1)

    minx = sys.maxsize
    maxx = 0
    miny = sys.maxsize
    maxy = 0

    # open input file
    # TODO check user inputed an arg
    with open(sys.argv[1], newline='') as fh:
        reader = csv.reader(fh, delimiter=',')
        for line in reader:
            # get bounding box in sub(?) pixels
            # TODO convert to pixels
            x1, x2, y1, y2 = [int(i) for i in line[1:5]]
            text = line[15]
            minx = min(minx, x1)
            maxx = max(maxx, x2)
            miny = min(miny, y1)
            maxy = max(maxy, y2)
            logging.debug("adding word %s at %d,%d %d wide and %d tall", text,
                          x1, y1, x2 - x1, y2 - y1)

            # get color
            # set default to red (shouldn't occur)
            color = "r"
            # check if all caps
            if text.isupper():
                color = "g"
            # check if all lowercase
            elif text.islower():
                color = "b"
            # check if only first letter is capatilized
            elif text.istitle():
                color = "m"
            # check if is a number
            elif text.replace('.', '', 1).isdigit():
                color = "c"
            else:
                logging.info("not sure what to do with '%s'", text)

            r = patches.Rectangle((x1, y1),
                                  x2 - x1,
                                  y2 - y1,
                                  linewidth=1,
                                  edgecolor=color,
                                  facecolor='none')

            ax.add_patch(r)

    plt.axis([minx - 100, maxx + 100, miny - 100, maxy + 100])

    plt.show()


if __name__ == "__main__":
    main()
