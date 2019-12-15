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
import os
import math

logging.basicConfig(level=logging.INFO)

colorMap = {1:'b', 2:'g', 3:'r', 4:'c', 5:'m', 0:'y'}

def getColumnDelimiters(d_f):
    #load x and y cordinates

    #get max and min x-values
    x_vals = sorted(d_f.x1.values)
    x_min = x_vals[int(.01*len(x_vals))]
    x_max = x_vals[int(.99*len(x_vals))]
    width = x_max - x_min


    if(width < 200):
        return

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
    try:
        col['y_center'] = col.apply(lambda t: (t.y1 + t.y2)/2, axis=1)
    except:
        return pd.DataFrame()
    y_cntrs_flat = col.y_center.values

    wordHeights = [row.y2 - row.y1 for _, row in col.iterrows()]
    medianWordHeight = np.median(wordHeights)

    sortedWordsHeights = sorted(wordHeights)

    height_p01 = sortedWordsHeights[int(len(sortedWordsHeights)*.01)]
    height_p99 = sortedWordsHeights[int(len(sortedWordsHeights)*.99)]

    for i in range(len(wordHeights)):
        if(wordHeights[i] <= height_p01 or wordHeights[i] >= height_p99):
            y_cntrs_flat[i] = None

    y_cntrs_pruned = y_cntrs_flat[~np.isnan(y_cntrs_flat)]

    y_cntrs_pruned = np.asarray(y_cntrs_pruned).reshape(-1, 1)

    try:
        if(y_cntrs_pruned.shape[0] <= 1):
            return pd.DataFrame()
    except:
        return pd.DataFrame()

    from scipy.cluster.hierarchy import fclusterdata
    y_pred = list(fclusterdata(y_cntrs_pruned, medianWordHeight*.5, criterion='distance'))

    rows = set(y_pred)


    for i in range(len(y_cntrs_flat)):
        if(np.isnan(y_cntrs_flat[i])):
            y_pred.insert(i, -1)

    col['LineLabel'] = y_pred

    row_heights = {t:col[col['LineLabel'] == t]['y_center'].mean() for t in rows}

    from collections import OrderedDict

    row_heights = OrderedDict(sorted(row_heights.items(), key=lambda x: x[1]))
    
    c = 1
    for i in row_heights.keys():
        row_heights[i] = (row_heights[i], c)
        c+=1

    row_heights[-1] = (-1, -1)

    col['LineLabel'] = col['LineLabel'].apply(lambda t: row_heights[t][1])
    
    def matchRow(x, val):
        i = 0
        diff = 1000000
        for i in range(len(x)):
            if abs(val - x[i][0]) < diff:
                diff = abs(val - x[i][0])
            else:
                return x[i-1][1]
            
    col['LineLabel'] = col.apply(lambda t: t.LineLabel if t.LineLabel != -1 else matchRow(list(row_heights.values()), (t.y1 + t.y2)/2), axis=1)

    return col.dropna()
    
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

def removeOutliers(page):
    xVals = page.x1.values
    xVals = sorted(xVals)
    gaps = [xVals[i+1] - xVals[i] for i in range(len(xVals)-1)]

    if(len(gaps) == 0):
        return page
    import statistics
    medGap = statistics.median(gaps)
    c = 0
    while gaps[c] > medGap*20:
        c+=1

    thresh = xVals[c]
    return page[page.x1 > thresh]

def swapping(scans, fname):
    rowCount = list(map(lambda t: len(t.LineLabel.unique()), scans))
    modeCount = None
    if(len(rowCount) == 0):
        print("hit0")
        return
    try:
        modeCount = statistics.mode(rowCount)
    except:
        modeCount = int(statistics.mean(rowCount))

    fScans = list(filter(lambda t: len(t.LineLabel.unique()) == modeCount, scans))

    swapped = []
    
    for i in range(1, modeCount+1):
        line = []
        rows = list(map(lambda t: t[t.LineLabel == i][['x1', 'x2', 'word']], fScans))

        if(len(rows) == 0):
            continue

        df = pd.DataFrame(columns=rows[0].columns)
        for j in rows:
            df = df.append(j, ignore_index = True)

        mean_width = df.apply(lambda t: t.x2-t.x1, axis=1).median()

        x_vals = df.x1.values.reshape(-1, 1)

        try:
            if(x_vals.shape[0] <= 1):
                continue
        except:
            continue
        from scipy.cluster.hierarchy import fclusterdata
        w_pred = list(fclusterdata(x_vals, mean_width*.25, criterion='distance'))
        df['label'] = w_pred
        
        word_pos = {t:df[df['label'] == t]['x1'].mean() for t in set(w_pred)}
  
        from collections import OrderedDict

        word_pos = OrderedDict(sorted(word_pos.items(), key=lambda x: x[1]))

        c = 1
        for j in list(word_pos.keys()).copy():
            word_pos[j] = c
            c+=1

        df['label'] = df['label'].apply(lambda t: word_pos[t])

        
        for j in range(1, len(set(w_pred)) + 1):
            words = df[df['label'] == j]['word'].values
            words = sorted(words, key=lambda t: len(str(t)), reverse=True)
            if len(words) < len(fScans)*.2:
                continue
            try:
                line.append(str(statistics.mode(words)))
            except:
                line.append(str(words[0]))
        swapped.append(" ".join(line))
    f = open(R"C:\Users\Remy Dahlke\Desktop\Capstone\Results\{}.txt".format(fname), "w")
    f.write("\n".join(swapped))
    f.close()

        

    
        



def main_sr(files, fname):
   
    scans = []


    for f in files[0:]:
        d_f = pd.read_csv(f, names=['x1', 'x2', 'y1', 'y2', 'word'], usecols=[1, 2, 3, 4, 15])
        if(d_f.shape[0] == 0):
            continue
        d_f = removeOutliers(d_f)

        colDelimiters = getColumnDelimiters(d_f)
        if colDelimiters == None:
            continue

        if len(colDelimiters) > 0:
            d_f = d_f[d_f.x2 <= colDelimiters[0]]

        scans.append(d_f)

    if(len(scans) == 0):
        return

    scans2 = []

    for i in range(len(scans)):
        zz = getLineCenters(scans[i])
        if(zz.shape[0] == 0):
            print("hit1")
            pass
        else:
            scans2.append(zz)

    swapping(scans2, fname)


def main():
    files = os.listdir(os.getcwd())
    files = list(filter(lambda t: ".day" in t, files))

    unq_f = set(list(map(lambda t: t.replace(".day", "")[0:-2], files)))
    unq_f = sorted(list(unq_f))
    
    for i in list(range(len(unq_f)))[73:]:
        print(i, unq_f[i])
        curr_f = list(filter(lambda t: unq_f[i] in t, files))
        main_sr(curr_f, unq_f[i])



import time
if __name__ == "__main__":
    start = time.time()
    main()
    print(round(time.time()-start,3))

