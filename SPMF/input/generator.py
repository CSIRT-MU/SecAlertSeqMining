#!/usr/bin/env python
""" Generate various types of input databases for SPMF library.
First argument is file name of the input file of alerts saved as json or csv.
Second argument is database type formatted as follows: [format].[data_type],
where format is name of the folder inside 'formats' folder,
and 'data_type' is name of the script inside the formats folder (without '.py' suffix).
Last argument denotes optional suffix of the output file.
Output file (database) is saved in the databases folder.
"""

import importlib
import pkgutil
import sys

import SPMF.input.formats
from SPMF.input.support.csv import Csv
from SPMF.input.support.idea import Idea


def import_modules(package, suffix):
    """ Import all modules from package and return them as list. """
    modules = []
    for _, name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(package.__name__ + "." + name)
        if hasattr(module, "read") and hasattr(module, "save") and module.__name__.endswith(suffix):
            modules.append(module)
    return modules


def import_module(package, module_name):
    return importlib.import_module(package.__name__ + "." + module_name)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) < 2:
        print("Missing arguments - input file name and db format [output suffix]", file=sys.stderr)
        return -1

    input_file = argv[0]
    db_format = argv[1]
    output_suffix = argv[2] if len(argv) >= 3 else ''

    # Ger Formatter object from module
    module = import_module(SPMF.input.formats, db_format)
    formatter = module.Formatter(output_suffix)

    # Get file type
    if input_file.endswith(".json"):
        idea_format = Idea
    elif input_file.endswith(".csv"):
        idea_format = Csv
    else:
        raise ValueError("Input file must be json or csv (file name has to end with '.csv' or '.json').")

    with open(input_file, "r") as file:

        print("Start reading the data.")
        # Read all events inside file
        counter = 0
        for line in file:
            counter += 1
            if counter == 1000000:
                print("1 000 000 lines processed")
                counter = 0

            idea = idea_format(line)
            formatter.read(idea)

        print("Reading done, going to save data")
        formatter.save()

    return 0


if __name__ == '__main__':
    status = main()
    sys.exit(status)
