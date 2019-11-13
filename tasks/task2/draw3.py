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

import numpy as np
import pandas as pd
import statistics

logging.basicConfig(level=logging.INFO)

colorMap = {1:'b', 2:'g', 3:'r', 4:'c', 5:'m', 0:'y'}

def getColumnDelimiters(d_f):
    #load x and y cordinates

    #get max and min x-values
    x_vals = sorted(d_f.x1.values)
    x_min = x_vals[int(.01*len(x_vals))]
    x_max = x_vals[int(.99*len(x_vals))]
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

def getLineCenters(col):
    col['y_center'] = col.apply(lambda t: (t.y1 + t.y2)/2, axis=1)
    y_cntrs_flat = col.y_center.values

    wordHeights = [row.y2 - row.y1 for _, row in col.iterrows()]
    medianWordHeight = np.median(wordHeights)

    sortedWordsHeights = sorted(wordHeights)

    height_p01 = sortedWordsHeights[int(len(sortedWordsHeights)*.01)]
    height_p99 = sortedWordsHeights[int(len(sortedWordsHeights)*.99)]

    for i in range(len(wordHeights)):
        if(wordHeights[i] <= height_p01 or wordHeights[i] >= height_p99):
            y_cntrs_flat[i] = None

    print(len(y_cntrs_flat))
    y_cntrs_pruned = y_cntrs_flat[~np.isnan(y_cntrs_flat)]

    y_cntrs_pruned = np.asarray(y_cntrs_pruned).reshape(-1, 1)


    

    from scipy.cluster.hierarchy import fclusterdata
    y_pred = list(fclusterdata(y_cntrs_pruned, medianWordHeight*.5, criterion='distance'))

    for i in range(len(y_cntrs_flat)):
        if(np.isnan(y_cntrs_flat[i])):
            y_pred.insert(i, -1)

    col['LineLabel'] = y_pred
    
    _, ax = plt.subplots(1)

    for _, row in col.iterrows():
        clr = row.LineLabel % 6
        r = patches.Rectangle((row.x1, row.y1),
            row.x2 - row.x1,
            row.y2 - row.y1,
            linewidth=.5,
            facecolor='none', 
            edgecolor=colorMap[clr]
        )

        ax.add_patch(r)
        ax.annotate(str(row.LineLabel), (row.x1, row.y1), fontsize=6)
    
    plt.axis([col.x1.min() - 100, col.x2.max() + 100, col.y1.min() - 100, col.y2.max() + 100])
    #plt.scatter(col.x1.values, col['y_center'].values, c=col['LineLabel'].values, marker = '.')

    plt.show(row.LineLabel)


    return




def main():
    """ Creats a graph of the input file words"""
    logging.debug("openning file %s", sys.argv[1])

    d_f = pd.read_csv(sys.argv[1], names=['x1', 'x2', 'y1', 'y2'], usecols=[1, 2, 3, 4])

    #call getColumnDelimiters
    colDelimiters = getColumnDelimiters(d_f)

    y_c = getLineCenters(d_f[d_f.x2 <= colDelimiters[0]])


    return

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
    for i in colDelimiters:
        t = patches.ConnectionPatch((i, miny), (i, maxy), coordsA="data")
        ax.add_patch(t)

    plt.axis([minx - 100, maxx + 100, miny - 100, maxy + 100])


    plt.show()

import time
if __name__ == "__main__":
    start = time.time()
    main()
    print(round(time.time()-start,3))