#!/usr/bin/env python3
import logging
import sys

import dayToDF
import getTitles as oneCol

def getTitles(year):
    dr = dayToDF.DayReader(year)
    cols = dr.cols()
    while cols is not None:
        print("Parsing pages with {} columns, starting with page {}".format(cols, dr.page()))
        if cols == 1:
            titles = oneCol.getTitles(dr.lines)
            if titles is not None:
                print(titles)
        elif cols == 2:
            for line in dr.lines():
                pass #print(line)
        elif cols == 3:
            for line in dr.lines():
                pass #print(line)
        else:
            logging.error("Page with %d columns, don't know what to do", cols)
            for line in dr.lines():
                pass #print(line)

        cols = dr.cols()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: %s YEAR", __file__) #DAYFILE [DAYFILE [...]]", __file__)
        sys.exit(1)
    sys.exit(getTitles(sys.argv[1]))
