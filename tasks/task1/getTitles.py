import sys


def main():
    with open(sys.argv[1]) as fh:
        for line in fh:
            if line.isupper() and not any(
                    char.isdigit()
                    for char in line) and len(line.split()) >= 2:
                print(line, end='')


if __name__ == '__main__':
    sys.exit(main())
