#!/usr/bin/env python3
"""
Code to generates a datafram from .day ocr files
With example code that iterates through lines of the scaned page
"""
import logging
import sys

import numpy as np
import pandas as pd

import nav

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

    # TODO this function can probably be substantially sped up

    def gaps(df):
        """
        All x values not contained in any words
        e.g. gaps between columns

        input: dataframe representing a page, with columns x{min,max}
        output: list [int] of x values that are not in any words
        """
        # know edge of left most word is not a gap, so skip it
        #gaps = list(range(int(df['xmin'].min() + 1), int(df['xmax'].max())))

        # remove each column of pixels where text exists
        gaps = (i for i in range(int(df['xmin'].min() + 1), int(df['xmax'].max())) if not df.loc[(df['xmin'] <= i) & (df['xmax'] >= i)].empty)

        return gaps

    def col_edges(df):
        """
        Generator of the x min and max that define the edge of a column
        input: dataframe, with columns x{min,max}
        output: generator [int, int] x min,max values for a column
        """
        # set start to left most char on page
        start = df['xmin'].min()
        for gap in gaps(df):
            # if there is space between start and gap must be a column
            if start != gap - 1:
                yield [start, gap]
            start = gap
        # append last column
        yield [start, df['xmax'].max()]

    # add col column, with -1 as default
    df['col'] = -1
    # for each column, update col value for words in that column
    for i, column in enumerate(col_edges(df)):
        # iter through words not already assigned to a col
        df.loc[(df['col'] == -1) & (df['xmin'] >= column[0]) & (df['xmax'] <= column[1]), 'col'] = i
    # check if any cols have a really small number of words
    # if they do, are probably mistakes from OCR so drop col
    for i in range(df['col'].max() + 1):
        col = df[df['col'] == i]
        if len(col) < len(df)/10:
            df = df.drop(col.index)
            df.loc[df['col'] > i, 'col'] -= 1
    return df


def _get_lines(df):
    """
    Figures out which line each word is on
    input: df, required columns: y{min,max}, col
    output: df, same as input but with added column: line

    lines are defined per column, i.e. there is a line 1 in column 1 and 2,
        but they are different
    """

    # TODO this function can definetly be improved, does a passible job but
    # often gets it wrong

    def height(word):
        """
        Returns a scaled y min,max value for the given word
        input: row from dataframe, with columns y{min,max}
        output: bottom, top (int, int), representing bottom/top of word
        """
        avg = (word['ymin'] + word['ymax']) / 2
        radius = (avg - word['ymin']) * .2
        return avg - radius, avg + radius

    def in_interval(l, miny, maxy):
        """
        returns if the given {min,max}y fall within the given line
        input: line [miny, maxy], {min,max}y of word. ([int, int] int, int)
        output: boolean, true if in interval, else false
        """
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
            miny, maxy = height(word)
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
    """Figures out order of words in each line

    Args:
        df (pandas.Dataframe): Requred columns: x{min,max}, line, col

    Returns:
        pandas.Dataframe: Same as input but with added column: word
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
    """Reads given day file, and return a dataframe describing it

    Args:
        fn (str): FilePath to a .day file

    Returns:
        pandas.DataFrame: Dataframe describing said .day file
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
    df = df.astype({'col': 'int32', 'line': 'int32', 'word': 'int32',
                    'xmin': 'int32', 'xmax': 'int32', 'ymin': 'int32',
                    'ymax': 'int32', 'text': 'str'})
    return df


def iter_df(df):
    """Generator that iterates row by row over df

    Args:
        df (pandas.DataFrame): Containing columns text, word, line, col

    Yields:
        str: Each str is a line in the df
    """
    # iter over cols
    for i in range(df['col'].max() + 1):
        col = df[df['col'] == i]
        # iter over lines
        for j in range(col['line'].max() + 1):
            line = col[col['line'] == j]
            # add words to string in order
            cur_line = line[line['word'] == 0].iloc[0]['text']
            for k in range(1, line['word'].max() + 1):
                word = line[line['word'] == k]
                cur_line += ' ' + word.iloc[0]['text']
            # return a line at a time
            yield cur_line


class DayReader:
    """Manages complicated day file parsing

    Can parse through a years day files, splitting by change in # of cols, not
    page end. This is potentially usefull for parsing, as sometimes a company
    info wraps to the next page but it does not appear they will wrap to a
    different column style page

    Note:
        Will raise an FileNotFoundError if no day files are found
    """
    def __init__(self, year, **kwargs):
        logging.debug("Creating DayReader for year %s", year)
        self._kwargs = kwargs  # for passing options to nav
        self._year = year  # manual year to look at
        self._pages = self._next_page()  # page df generator
        self._page_name = None  # name of current page
        try:
            self._df = next(self._pages)  # current page df
        except StopIteration:
            raise FileNotFoundError("No day files were found")
        self._cols = self._df['col'].max() + 1  # num cols on curr page

    def __iter__(self):
        while self._df is not None:
            yield self._cols, self._lines

    def _lines(self):
        """yield manual line by line, until change in # of cols

        Yields:
            str: next line in manual

        Note:
            When the end of a page is reached, if the next page has a different
            number of columns this method will return None instead of
            continuing, but can be called again immediately
        """
        # iter over lines in current page
        for l in iter_df(self._df):
            yield l
        # iter over pages in order
        for page in self._pages:
            self._df = page
            cols = self._df['col'].max() + 1
            # check if new page has same number of cols as last
            if self._cols != cols:
                # if it doesn't update self._cols and return
                logging.debug(
                    "End of pages with %d columns, next page has %d columns",
                    self._cols, cols)
                self._cols = cols
                return
            # iter over lines in page
            for l in iter_df(page):
                yield l
        # Out of pages, so set everything to None to stop weird behavior
        self._cols = None
        self._page_name = None
        self._df = None
        self._pages = None

    def page(self):
        """Returns the current page filepath

        Returns:
            str: filepath for current page
        """
        return self._page_name

    def _next_page(self):
        """Moves on to next page in manual

        Returns:
            Generator[pandas.DataFrame]: each df is the next page in the manual
        """
        for p in nav.pages(self._year, **self._kwargs):
            logging.debug("Moving to next page, %s", p)
            self._page_name = p
            yield get_df(p)


def _main(args):
    """Prints out text for all given .day files

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


if __name__ == '__main__':
    sys.exit(_main(sys.argv[1:]))
