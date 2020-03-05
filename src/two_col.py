#!/usr/bin/env python3
"""Program generates text files from .day ocr files"""
import logging
import sys
from enum import Enum, auto
import copy
import numpy as np
import pandas as pd
import re

#import draw





def readDay(filepath):
    """
    reads in the given filepath for a .day file into a pandas df
    input: str, filepath to .day file
    output: dataframe, representing all words in the .day file
    """
    df = pd.read_csv(filepath,
                     names=["xmin", "xmax", "ymin", "ymax", "text"],
                     usecols=[1, 2, 3, 4, 14],
                     dtype={
                         "xmin": np.int32,
                         "xmax": np.int32,
                         "ymin": np.int32,
                         "ymax": np.int32,
                         "text": str
                     })
    # can't work with rows that don't have these things, so drop them
    df.dropna(inplace=True)

    # FIXME find better way to get rid of page title
    df = df.iloc[4:]

    # convert to pixel space
    for col in ['xmin', 'xmax', 'ymin', 'ymax']:
        df[col] *= 400 / 1440
    return df





def main():
    # Read .day into a df
    # add column to df, specifying type of each element (currently all words)
    # add column to df, specifiying each words column
    # add column to df, specifying each words line
    # add column to df, specifying word order (left to right)
    # print in correct order
    if len(sys.argv) < 2:
        logging.error("Usage: %s FILE, where FILE is a .day filepath",
                      __file__)
        return 1

    lastline = "MISSED COMPANY NAME"
    box = None
    for fn in sys.argv[1:]:
        # read in .day file
        df = readDay(fn)
        # set all elements to be words
        node=[]
        for i in range(len(df)-1):
            if (df['xmax'].iloc[i]>df['xmax'].iloc[i+1] and df['ymax'].iloc[i]<df['ymax'].iloc[i+1]) or df['xmax'].iloc[i]>df['xmin'].iloc[i+1]:
                node.append(i)
        line_1=[]
        line_1.append(df['text'].iloc[node[0]])
        for i in range(len(node)-1):
            line_1.append(df['text'].iloc[node[i]+1:node[i+1]+1].values.tolist())
        result=[]
        for i in range(len(line_1)-1):
            if line_1[i][0].isupper():
                if "Incorporated" in line_1[i] or "Incor-" in line_1[i] or "Inco-" in line_1[i] or "Incorp-" in line_1[i] or "Incorpo-" in line_1[i] or "Incorpor-" in line_1[i] or "Incorpora-" in line_1[i] or "Incorporat-" in line_1[i] or "Incorporate-" in line_1[i] or "(Controlled" in line_1[i] or "Cont-" in line_1[i] or "In-" in line_1[i] or "Organized" in line_1[i] or "Incorporated" in line_1[i+1] or "incorporated" in line_1[i]:
                    result.append(line_1[i])
        final_result=[]
        for i in result:
            upper= [word for word in i if word.isupper()]
            #final_result.append(upper)
            print(upper)
        #print(final_result)
        min_coor=[]
        max_coor=[]
        for i in range(len(final_result)):
            min_coor.append(df.loc[df['text'] == final_result[i][0],['xmin','ymin']].values.tolist())
            max_coor.append(df.loc[df['text'] == final_result[i][len(final_result[i])-1],['xmax','ymax']].values.tolist())
        #print(min_coor)
        #print(max_coor)

                
            

   
    """
    p = draw.Plot()
    if len(sys.argv) == 3:
        p.setImage(sys.argv[2])
    c = ['b', 'g', 'r', 'c', 'm', 'k']
    for i, row in df.loc[df['type'] == elemType.line].iterrows():
        p.addRectangle([row['xmin'], row['ymin']], [row['xmax'], row['ymax']],
                       c[i % len(c)])
    p.show()
    """


if __name__ == '__main__':
    sys.exit(main())