#!/usr/bin/env python3
"""Program generates text files from .day ocr files"""
import logging
import sys

import numpy as np
import pandas as pd

# import draw


def _read_day(filepath):
    """
    reads in the given filepath for a .day file into a pandas df
    input: str, filepath to .day file
    output: dataframe, representing all words in the .day file
        with columns: xmin(int32), xmax(int32), ymin(int32),
            ymax(int32), text(str)
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
    # can't work with rows that don't have these things, so drop them
    df.dropna(inplace=True)

    # FIXME find better way to get rid of page title
    df = df.iloc[4:]

    # convert to pixel space
    for col in ['xmin', 'xmax', 'ymin', 'ymax']:
        df[col] *= 400 / 1440
    return df


def _get_cols(df):
    """
    Figures out which columns words are in, and adds that as a col in df
    input: df of words, required columns: {x,y}{min,max}
    output: df, same as input but with an extra column: col, representing which
        col element is in
    """

    # TODO make faster

    # check all (ish) x values if gap
    # don't care about ish-ness since gap won't be at edge of page

    # list out all pixels that might contain a gap
    # can exclude first/last 20 pixels as there won't be a gap that
    #    close to the edge
    # TODO fix magic number (20)
    gaps = list(range(int(df['xmin'].min() + 20), int(df['xmax'].max() - 20)))

    # remove each column of pixels where text exists
    for _, word in df.iterrows():
        for i in gaps[:]:
            if word['xmin'] < i < word['xmax']:
                gaps.remove(i)
                continue

    # leaving only pixels that are gaps in "gaps"

    intervals = []
    # set start to left most char on page
    start = df['xmin'].min()
    for gap in gaps:
        # if there is space between start and gap must be a column
        if start != gap - 1:
            intervals.append([start, gap])
        start = gap
    # append last column
    intervals.append([start, df['xmax'].max()])

    # add col column, with -1 as default
    df['col'] = -1
    # for each column, update col value for words in that column
    for i, column in enumerate(intervals):
        # iter through words not already assigned to a col
        for j, word in df.loc[df['col'] == -1].iterrows():
            # if word in column, update its col value
            if word['xmin'] >= column[0] and word['xmax'] <= column[1]:
                df.loc[j, 'col'] = i

    return df


def _get_lines(df):
    """
    Figures out which line each word is on
    input: df, required columns: y{min,max}, col
    output: df, same as input but with added column: line

    lines are defined per column, i.e. there is a line 1 in column 1 and 2,
        but they are different
    """

    def heights(row):
        avg = (row['ymin'] + row['ymax']) / 2
        radius = (avg - row['ymin']) * .2
        return avg - radius, avg + radius

    def in_interval(l, miny, maxy):
        # word starts before interval, and ends within it
        if (l[0] <= miny <= l[1]) and maxy >= l[1]:
            return True
        # word starts in interval, but ends after it
        elif l[0] >= miny and (l[0] <= maxy <= l[1]):
            return True
        # word starts before interval and ends after it
        elif l[0] <= miny and maxy <= l[1]:
            return True
        # word contained in interval
        elif l[0] >= miny and maxy >= l[1]:
            return True
        return False

    # add line column, with -1 as default
    df['line'] = -1
    # iterate over each column
    for i in range(df['col'].max() + 1):
        lines = []
        # FIXME assumes lines are added in order, not necessarily true
        # iterate over words in column adding words to a line
        for j, word in df.loc[df['col'] == i].iterrows():
            # get y min/max of word
            miny, maxy = heights(word)
            # if word fits in an existing line, update its line value
            for k, l in enumerate(lines):
                if in_interval(l, miny, maxy):
                    lines[k][0] = min(l[0], miny)
                    lines[k][1] = max(l[1], maxy)
                    df.loc[j, 'line'] = k
                    break
            # otherwise add a new line and update words line value
            if df.loc[j, 'line'] == -1:
                df.loc[j, 'line'] = len(lines)
                lines.append([miny, maxy])

    return df


def _get_word_order(df):
    """
    Figures out order of words in each line
    input: df, requred columns: x{min,max}, line, col
    output: df, same as input but with added column: word
    """
    # add word column, with default -1
    df['word'] = -1
    for i in range(df['col'].max() + 1):
        for j in range(df['line'].max() + 1):
            words = df.loc[(df['col'] == i) & (df['line'] == j)].iterrows()
            words = sorted(list(words), key=lambda x: x[1]['xmin'])

            for order, w in enumerate(words):
                df.loc[w[0], 'word'] = order
    return df


def get_df(fn):
    """
    Reads given day file, and return a dataframe describing it
    input: filepath(str), path to a .day file
    output: df, a dataframe describing said .day file
        with rows: {x,y}{min,max}, col, line, word
        where col, line, and word give the ordering on the page
        e.x: col=1,line=2,word=0 is the first word of the third line of
            the second column
    """
    # read in .day file
    df = _read_day(fn)
    # split into columns
    df = _get_cols(df)
    # split into lines
    df = _get_lines(df)
    # figure out order of words
    df = _get_word_order(df)
    return df


def iter_df(df):
    """
    iterator that iterates row by row over df
    input: df, containing cols text, word, line, col
    output: yields strings, each is a line in the df
    """
    # iter over cols
    for i in range(df['col'].max() + 1):
        col = df[df['col'] == i]
        # iter over lines
        for j in range(col['line'].max() + 1):
            line = col[col['line'] == j]
            # add words to string in order
            cur_line = line[line['word'] == 0].iloc[0]['text']
            for k in range(line['word'].max() + 1):
                word = line[line['word'] == k]
                cur_line += ' ' + word.iloc[0]['text']
            # return a line at a time
            yield cur_line


def _main(args):
    """
    Prints out text for all given .day files
    example usage of get_df and iter_df
    """
    if len(args) < 1:
        logging.error("Usage: %s FILE, where FILE is a .day filepath",
                      __file__)
        return 1

    for fn in args:
        df = get_df(fn)
        for line in iter_df(df):
            print(line)
    return 0

#    code to print boxes over .tif file, helpfull for debugging
#    p = draw.Plot()
#    if len(sys.argv) == 3:
#        p.setImage(sys.argv[2])
#    c = ['b', 'g', 'r', 'c', 'm', 'k']
#    for i, row in df.loc[df['type'] == elemType.line].iterrows():
#        p.addRectangle([row['xmin'], row['ymin']], [row['xmax'], row['ymax']],
#                       c[i % len(c)])
#
#    p.show()


if __name__ == '__main__':
    sys.exit(_main(sys.argv[1:]))
