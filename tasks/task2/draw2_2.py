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

import pandas as pd
import statistics

logging.basicConfig(level=logging.INFO)

def getColumnDelimiters(fName):
    #load x and y cordinates
    d_f = pd.read_csv(fName, names=['x1', 'x2', 'y1', 'y2'], usecols=[1, 2, 3, 4])
    #get max and min x-values
    x_min = d_f.x1.min()
    x_max = d_f.x2.max()
    width = x_max - x_min

    """ creates dictionary of 200 evenly spaced candidate verticles
        that will eventually count the number of 
        word intersections per verticle
    """
    #buffers from the edge by 5% on each edge
    verticles = {t : 0 for t in range(x_min+int(width*.05), x_max-int(width*.05), int(width/200))}
    
    #count number of word intersections for each candidate verticle
    for i in verticles:
        verticles[i] = d_f[(d_f.x1 <= i) & (i <= d_f.x2)].shape[0]

    #finds mean and standard deviation of candidate verticles
    intsctMean = statistics.mean(list(verticles.values()))
    intsctStd = statistics.stdev(list(verticles.values()))
    columnSeperatorXVals = []

    temp = []
    """ finds adjacent verticles with a z-score 
        less than -3 of intersections and takes the median 
        as the column threshhold    
    """
    for i in verticles:
        if((verticles[i]-intsctMean)/intsctStd <= -3):
            temp.append(i)
        else:
            if temp != []:
                medianTemp = statistics.median(temp)
                columnSeperatorXVals.append(medianTemp)
            temp = []
    return columnSeperatorXVals

def getlineDelimiters(fName):
    #load x and y cordinates
    d_f = pd.read_csv(fName, names=['x1', 'x2', 'y1', 'y2'], usecols=[1, 2, 3, 4])
    y_max = d_f.y2.max()
    x_min = d_f.x1.min()
    """the idea for split the line: first, we find the max of y to get the highest, 
                and then diego said we need to minus 10 pixel to draw the line. And that will give us the first line.
                Next, find the local max which smaller than that line y_value. Set up that one as the "highest", and - 10 pixel
                as the new line. Draw the line in this method until touching the bottom of the page"
    """


    """sudo code
    draw_line_y = y_max - 10 #inital the first line from the top  
    while draw_line_y > 0:
        find the max of y which smaller than draw_line_y
        draw_line_y = max of y -10
        list_line.append(draw_line_y)
    return list_line
    """





    

def main():
    """ Creats a graph of the input file words"""
    logging.debug("openning file %s", sys.argv[1])

    #call getColumnDelimiters
    columnDelimiters = getColumnDelimiters(sys.argv[1])
    lineDelimiters = getlineDelimiters(sys.argv[1])

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
                #logging.info("not sure what to do with '%s'", text)
                pass

            r = patches.Rectangle((x1, y1),
                                  x2 - x1,
                                  y2 - y1,
                                  linewidth=1,
                                  edgecolor=color,
                                  facecolor='none')

            ax.add_patch(r)
    
    #write black lines for deliminters
    for i in columnDelimiters:
        t = patches.ConnectionPatch((i, miny), (i, maxy), coordsA="data")
        ax.add_patch(t)

    """for i in lineDelimiters:
            plt.plot([x_min, list_line[i]],[midval, list_line[i]])
    """

    plt.axis([minx - 100, maxx + 100, miny - 100, maxy + 100])

    print("X-values for Column Seperations:", columnDelimiters)

    plt.show()


if __name__ == "__main__":
    main()