#!/usr/bin/env python3

import sys


def main():
    with open(sys.argv[1]) as fh:
        lastline = ''
        for line in fh:
            l = line.strip()
            if l.startswith('History'):
                print("'"+lastline+"'", end=', ')
                lastline="MISSED COMPANY NAME"
            if l.isupper():
                lastline = l

if __name__ == '__main__':
    sys.exit(main())
