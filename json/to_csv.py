"""
    Convert json IDEA alerts to csv. Pass name of input file as argument.
    Input file should contain one IDEA alert per line.
    Output csv entries are printed to stdout.
"""

import sys
from SPMF.input.support.idea import Idea


def none_to_empty_str(o):
    return str(o) if o else ""


def process_line(line):
    idea = Idea(line)
    return ",".join(map(none_to_empty_str,
                        [idea.id,
                         idea.aggr_id,
                         idea.time,
                         idea.category,
                         idea.source,
                         idea.src_proto,
                         idea.target,
                         idea.tar_proto,
                         idea.port,
                         idea.conn_count,
                         idea.sensor]))


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) < 1:
        print("Missing arguments - input file name", file=sys.stderr)
        return -1

    file_name = argv[1]

    # Load alerts
    with open(file_name, 'r') as file:
        for line in file:
            print(process_line(line))


if __name__ == '__main__':
    status = main()
    sys.exit(status)
