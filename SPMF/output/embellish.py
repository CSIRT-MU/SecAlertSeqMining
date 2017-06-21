""" Make rules and patterns more readable.
"""
import fileinput
import sys


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) < 1:
        print("Missing arguments - input file name", file=sys.stderr)
        return -1

    file_name = argv[0]

    for line in fileinput.input(file_name, inplace=1):
        new_line = line.replace("Recon.Scanning", "Scan") \
            .replace("-1  #SUP", " #SUP") \
            .replace("-1 #SUP", " #SUP") \
            .replace("-1", "->")

        print(new_line, end='')


if __name__ == '__main__':
    status = main()
    sys.exit(status)
