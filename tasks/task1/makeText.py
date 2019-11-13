#!/usr/bin/env python3
"""Program generates text files from .day ocr files"""
import logging
import sys
from enum import Enum, auto

import numpy as np
import pandas as pd

import draw


class elemType(Enum):
    word = auto()
    col = auto()
    line = auto()


def readDay(filepath):
    """
    reads in the given filepath for a .day file into a pandas df
    input: str, filepath to .day file
    output: dataframe, representing all words in the .day file
    """
    df = pd.read_csv(filepath,
                     names=["xmin", "xmax", "ymin", "ymax", "text"],
                     usecols=[1, 2, 3, 4, 15],
                     dtype={
                         "xmin": np.int32,
                         "xmax": np.int32,
                         "ymin": np.int32,
                         "ymax": np.int32,
                         "text": str
                     })
    df.dropna(inplace=True)

    # FIXME find better way to get rid of page title
    df = df.iloc[4:]
    # convert to pixel space
    for col in ['xmin', 'xmax', 'ymin', 'ymax']:
        df[col] *= 400 / 1440
    return df


def getCols(df):
    """
    Adds column to df specifying which column each element is in
    input: df of words, required columns: {x,y}{min,max}
    output: df, same as input but with an extra column: col, representing which
        col element is in

    assumes all elements are words
    """
    df['col'] = 0

    # check all (ish) x values if gap
    # don't care about ish-ness since gap won't be at edge of page

    gaps = [
        x
        for x in range(int(df['xmin'].min() + 20), int(df['xmax'].max() - 20))
    ]
    i = gaps[0]
    for _, row in df.iterrows():
        for i in gaps[:]:
            if i > row['xmin'] and i < row['xmax']:
                gaps.remove(i)
        if len(gaps) == 0:
            # FIXME
            return df
            col = {
                'xmin': df['xmin'].min(),
                'xmax': df['xmax'].max(),
                'ymin': df['ymin'].min(),
                'ymax': df['ymax'].max(),
                'type': elemType.col,
                'col': 0
            }
            df = df.append(pd.DataFrame(col), ignore_index=True)
            return df

    gapIntervals = []
    gapStart = df['xmin'].min()
    for gap in gaps:
        if gapStart != gap - 1:
            gapIntervals.append([gapStart, gap])
        gapStart = gap
    gapIntervals.append([gapStart, df['xmax'].max()])

    cols = []

    for i, col in enumerate(gapIntervals):
        for j, row in df.loc[df['col'] == 0].iterrows():
            if row['xmin'] >= col[0] and row['xmax'] <= col[1]:
                df.loc[j, 'col'] = i

        col = {
            'xmin': col[0],
            'xmax': col[1],
            'ymin': df.loc[df['col'] == i]['ymin'].min(),
            'ymax': df.loc[df['col'] == i]['ymax'].max(),
            'type': elemType.col,
            'col': i
        }
        cols.append(col)
    df = df.append(pd.DataFrame(cols), ignore_index=True)

    return df


def getLines(df):
    """
    Figures out which line each word is on
    input: df, required columns: y{min,max}, [col], [type]
    output: df, same as input but with added column: line

    lines are defined per column, i.e. there is a line 1 in column 1 and 2, but they are different
    """

    def heights(row):
        avg = (row['ymin'] + row['ymax']) / 2
        radius = (avg - row['ymin']) * .2
        return avg - radius, avg + radius

    def inInterval(l, miny, maxy):
        if (l[0] <= miny and l[1] >= miny) and l[1] <= maxy:
            return True
        elif l[0] >= miny and (l[0] <= maxy and l[1] >= maxy):
            return True
        elif l[0] <= miny and l[1] >= maxy:
            return True
        elif l[0] >= miny and l[1] <= maxy:
            return True
        return False

    df['line'] = -1
    # iterate over each column
    for i in range(df['col'].max() + 1):
        lines = []
        for j, row in df.loc[(df['col'] == i)
                             & (df['type'] == elemType.word)].iterrows():
            miny, maxy = heights(row)
            for k, l in enumerate(lines):
                if inInterval(l, miny, maxy):
                    lines[k][0] = min(l[0], miny)
                    lines[k][1] = max(l[1], maxy)
                    df.loc[j, 'line'] = k
                    break
            if df.loc[j, 'line'] == -1:
                df.loc[j, 'line'] = len(lines)
                lines.append([miny, maxy])

        # add line boxes to df
        ls = []
        for j, l in enumerate(lines):

            newl = {
                'xmin':
                df.loc[(df['col'] == i) & (df['line'] == j)]['xmin'].min(),
                'xmax':
                df.loc[(df['col'] == i) & (df['line'] == j)]['xmax'].max(),
                'ymin':
                df.loc[(df['col'] == i) & (df['line'] == j)]['ymin'].min(),
                'ymax':
                df.loc[(df['col'] == i) & (df['line'] == j)]['ymax'].max(),
                'type': elemType.line,
                'col': i,
                'line': j
            }
            ls.append(newl)
        df = df.append(pd.DataFrame(ls), ignore_index=True)

    return df


def getWordOrder(df):
    """
    Figures out order of words in each line
    input: df, requred columns: x{min,max}, [line], [type]
    output: df, same as input but with added column: word

    if line column not included assumes all elements are in same line
    if type column not included assumes all elements are words
    """
    df['word'] = 0
    for i in range(df['col'].max() + 1):
        for j in range(df['line'].max() + 1):
            words = []
            for k, w in df.loc[(df['type'] == elemType.word) & (df['col'] == i)
                               & (df['line'] == j)].iterrows():
                words.append([k, w])
            words = sorted(words, key=lambda x: x[1]['xmin'])

            for k, w in enumerate(words):
                df[w[0], 'word'] = k
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

    for fn in sys.argv[1:]:
        # read in .day file
        df = readDay(fn)
        # set all elements to be words
        df['type'] = elemType.word
        # split into columns
        df = getCols(df)
        # split into lines
        df = getLines(df)
        df = getWordOrder(df)
        for i in range(df['col'].max() + 1):
            for j in range(df['line'].max() + 1):
                for k, w in df.loc[(df['type'] == elemType.word)
                                   & (df['col'] == i)
                                   & (df['line'] == j)].iterrows():
                    print(w['text'], end=' ')
                print('')
            print('\n')
        print('\n\n')
    """
    p = draw.Plot()
    if len(sys.argv) == 3:
        p.setImage(sys.argv[2])
    c = ['b', 'g', 'r', 'c', 'm', 'k', 'w']
    for i, row in df.loc[df['type'] == elemType.line].iterrows():
        p.addRectangle([row['xmin'], row['ymin']], [row['xmax'], row['ymax']],
                       c[i % len(c)])

    p.show()
    """


if __name__ == '__main__':
    sys.exit(main())
