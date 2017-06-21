""" Decode indexes of items in various rules and patterns created by SPMF.
Search for all .txt files in current directory and try to replace numerical items with strings based on .map file.
Map file is seek by the name of input file and should be saved in SPMF/input/databases directories together with
the corresponding database.
"""

import fileinput
import os
import sys
import re

from SPMF.input.support.item_map import ItemMap


def main():
    # Find all txt files in current dir
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files = [f for f in os.listdir(current_dir) if os.path.isfile(f) and f.endswith(".txt")]

    for f in files:

        # Load map for specific file
        try:
            database = str(f).split('.')[0].split('_')
            database_type = database[0]
            database_name = database[1]
            item_map = ItemMap()
            item_map.load_map("../input/databases/{}/{}".format(database_type, database_name))
        except Exception as e:
            print("Cannot create map for file {}, because of: {}".format(f, e), file=sys.stderr)
            continue

        # Replace int to string due to map
        for line in fileinput.input(f, inplace=1):
            line_list = re.split(' |,', line)
            new_line = " ".join(map(item_map.index_to_str, line_list))
            sys.stdout.write(new_line)

    return 0


if __name__ == '__main__':
    status = main()
    sys.exit(status)
