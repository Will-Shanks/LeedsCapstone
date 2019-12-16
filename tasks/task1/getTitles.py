#!/usr/bin/env python3

import sys


def main():
    with open(sys.argv[1]) as fh:
        lastline = ''
        for line in fh:
            if line.startswith('History'):
                if lastline.isupper():
                    print(lastline, end='')
                else:
                    print("MISSED COMPANY NAME")
            lastline = line

if __name__ == '__main__':
    sys.exit(main())
