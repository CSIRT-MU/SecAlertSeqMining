#!/usr/bin/env python
import argparse
import importlib
import sys
import os
from typing import TextIO, Iterable


def main(input_file: TextIO, output_dir: str, db_format: str, db_types: Iterable[str], db_suffix: str):
    # Get input file format
    if input_file.name.endswith(".json"):
        from alerts.idea import Idea
        alert_format = Idea
    elif input_file.name.endswith(".csv"):
        from alerts.csv import Csv
        alert_format = Csv
    else:
        raise ValueError("Input file must be json or csv (file name has to end with '.csv' or '.json').")

    # Import database modules
    db_modules = [importlib.import_module(f"formats.{db_format}.{db_type}") for db_type in db_types]

    # Create database objects
    databases = [m.Database(output_dir, db_suffix) for m in db_modules]

    # Process alerts
    print("Start reading alerts.")
    for counter, line in enumerate(input_file, start=1):
        if counter % 1000 == 0:
            sys.stdout.write(f"\r{counter} alerts processed.")

        alert = alert_format(line)
        for db in databases:
            db.read(alert)

    print(f"\r{counter} alerts processed.")

    # Save databases
    print("Reading done, going to save databases.")
    for db in databases:
        print()
        print(f"Going to save database '{db.output_file_path()}' with {db.len_sequences()} sequences.")
        db.save()
        print("Database saved.")

    return 0


if __name__ == '__main__':

    def is_dir(path: str) -> str:
        if not os.path.isdir(path):
            raise argparse.ArgumentTypeError("Not a directory: '{}'".format(path))
        return path


    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Generate sequential databases in format required by SPMF library '
                                                 '(http://www.philippe-fournier-viger.com/spmf/).')
    parser.add_argument("-i", "--input-file",
                        required=True,
                        type=argparse.FileType('r', encoding='UTF-8'),
                        help="Path to input file containing alerts. Input file can be '.json' with IDEA alerts (one "
                             "json alert per line) or '.csv' with one alert per line and parameter order as defined in "
                             "databases/alerts/csv.py module.")
    parser.add_argument("-o", "--output-dir",
                        required=True,
                        type=is_dir,
                        help="Path to dir where generated databases will be stored.")
    parser.add_argument("--format",
                        choices=['basic', 'timed'],
                        default='basic',
                        help="Format of output databases. It's basically name of package in databases/formats/ folder. "
                             "You can check existing formats by looking at "
                             "databases/formats/{basic,timed}/abstract.py modules.")
    parser.add_argument("--db-types",
                        required=True,
                        nargs="+",
                        type=str,
                        help="Types of databases to be created - names of modules inside formats/{format}/ directory,"
                             " where {format} is folder specified by --format argument.")
    parser.add_argument("--db-suffix",
                        type=str,
                        help="Suffix which will be added to output database names.")
    args = parser.parse_args()

    status = main(args.input_file, args.output_dir, args.format, args.db_types, args.db_suffix)
    sys.exit(status)
