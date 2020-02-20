#!/usr/bin/env python3
"""
This script reads in the given file, and generates a graph of the words in it
usage: ./draw.py ocroutput.day
"""

import csv
import logging
import time
import sys

import matplotlib.patches as patches
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import statistics
import os
import math



def draw_df(col):
    col = col.copy()
    col.y1 = col.y1.apply(lambda t : -t)
    col.y2 = col.y2.apply(lambda t : -t)
    
    _, ax = plt.subplots(1)

    for _, row in col.iterrows():
        r = patches.Rectangle((row.x1, row.y1),
            row.x2 - row.x1,
            row.y2 - row.y1,
            linewidth=.5,
            facecolor='none', 
            edgecolor='b'
        )

        ax.add_patch(r)
        ax.annotate(str(row.word), (row.x1, row.y2), fontsize=7)
    
    plt.axis([col.x1.min() - 100, col.x2.max() + 100, col.y1.min() - 100, col.y2.max() + 100])

    plt.show()


    return

def removeOutliers_x(page):
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

    thresh1 = xVals[c]

    c = len(xVals) - 1

    while gaps[c-1] > medGap*20:
        c-=1
    
    thresh2 = xVals[c]

    page = page[page.x1 >= thresh1]
    page = page[page.x1 <= thresh2]
    return page

def removeOutliers_y(page):
    yVals = page.y1.values
    yVals = sorted(yVals)
    gaps = [yVals[i+1] - yVals[i] for i in range(len(yVals)-1)]

    if(len(gaps) == 0):
        return page
    medGap = statistics.median(gaps)
    c = 0
    while gaps[c] > medGap*20:
        c+=1

    thresh1 = yVals[c]

    c = len(yVals) - 1

    while gaps[c-1] > medGap*20:
        c-=1
    
    thresh2 = yVals[c]

    page = page[page.y1 >= thresh1]
    page = page[page.y1 <= thresh2]
    return page
       
def swap(sub_df):
    merged_df = pd.DataFrame(columns=sub_df.columns)
    for i in sub_df.cluster.unique():
        clust = sub_df[sub_df.cluster == i]
        guesses = clust.word.values
        mode_word = None

        from scipy import stats

        mode_word = stats.mode(guesses)[0][0]
        
        clust = clust.mean()
        clust.cluster = int(clust.cluster)
        clust['word'] = mode_word
        merged_df = merged_df.append(clust, ignore_index=True)
    return merged_df

    
def cluster(scans):
    from scipy.cluster.hierarchy import fclusterdata

    df = pd.DataFrame(columns=scans[0].columns)
    for i in scans:
        df = df.append(i, ignore_index=True)


    median_height = statistics.mean(df.apply(lambda t: (t.y2 - t.y1), axis=1).values)
    median_width = statistics.mean(df.apply(lambda t: (t.x2 - t.x1), axis=1).values)  
    scale = median_width/median_height

    df['y_center'] = df['y_center'].apply(lambda t: t*(scale))

    window = median_height*scale*6

    min_y = df.y1.min()*scale
    max_y = df.y2.max()*scale

    unified_df = pd.DataFrame(columns=list(scans[0].columns) + ['vote_count'])

    for i in range(int(min_y-1), int(max_y+1), int(window/2)):
        sub_df = df[(df.y_center >= i) & (df.y_center <= i + window)]

        if sub_df.shape[0] <= 1:
            continue

        word_centers = sub_df[['x_center', 'y_center']].values

        from collections import Counter
        
        clustering = list(fclusterdata(word_centers, median_width*.25, criterion='distance'))
        votes = Counter(clustering)

        sub_df['cluster'] = clustering

        too_small = [t for t in votes if votes[t] < len(scans)/2]

        sub_df = sub_df[~sub_df.cluster.isin(too_small)]

        swapped_df = swap(sub_df)
        swapped_df['vote_count'] = swapped_df['cluster'].apply(lambda t: votes[int(t)])
        swapped_df = swapped_df.drop(columns=['cluster'])

        unified_df = unified_df.append(swapped_df, ignore_index=True)


    word_centers = unified_df[['x_center', 'y_center']].values

    if unified_df.shape[0] == 0:
        return unified_df

    clustering = list(fclusterdata(word_centers, median_width*.25, criterion='distance'))

    unified_df['clust'] = clustering

    final_df = pd.DataFrame(columns=unified_df.columns)

    for i in set(clustering):
        group = unified_df[unified_df.clust == i]
        group = group.sort_values(by=['vote_count'], ascending=False)
        final_df = final_df.append(group.head(1), ignore_index=True)

    final_df = final_df.drop(columns=['clust', 'x_center', 'y_center', 'vote_count'])
    

    return final_df




def main_sr(files, fname):
   
    scans = []


    for f in files[:]:
        d_f = pd.read_csv(f, names=['x1', 'x2', 'y1', 'y2', 'word'], usecols=[1, 2, 3, 4, 14])

        d_f = d_f.dropna()

        d_f['word'] = d_f.word.apply(lambda t: str(t))


        d_f = removeOutliers_x(d_f)
        d_f = removeOutliers_y(d_f)


        d_f['x_center'] = d_f.apply(lambda t: (t.x1 + t.x2)/2.0, axis=1)
        d_f['y_center'] = d_f.apply(lambda t: (t.y1 + t.y2)/2.0, axis=1)

        scans.append(d_f)

    final_df = cluster(scans)
    cols = ['x1', 'x2', 'y1', 'y2']
    for i in cols:
        final_df[i] = final_df[i].apply(lambda t: int(t))

    if final_df.shape[0] == 0:
        return

    #draw_df(final_df)
    get_end = lambda x: x[x.rindex("/")+1:]

    fname = get_end(fname)

    final_df.to_csv("/projects/reda2367/output/" + fname + "_u.day", header=False, index=False)#where the files write to



def main():
    import glob

    files = glob.glob("/scratch/summit/diga9728/Moodys/Industrials/OCRrun1930/*/OCRoutputIndustrial19300015-008*.day")#path of source day here
    files = list(filter(lambda t: ".day" in t, files))

    unq_f = set(list(map(lambda t: t.replace(".day", "")[0:-2], files)))
    unq_f = sorted(list(unq_f))
    
    for i in list(range(len(unq_f)))[:]:
        print(i, unq_f[i])
        curr_f = list(filter(lambda t: unq_f[i] in t, files))

        main_sr(curr_f, unq_f[i])



if __name__ == "__main__":
    start = time.time()
    main()
    print(round(time.time()-start,3))

