""" Process support or confidence of file given as first argument.

This script can do two different things based on the passed arguments:

    * If just one argument (input file) is present, the confidence will be rounded to 5 decimals.

    * If there is a second argument (number - sum of transactions in input database), then support will be divided
      by the sum and a original support value will be preserved in brackets after this value.

"""

import fileinput
import sys

SUPP_TOKEN = "#SUP: "
CONF_TOKEN = "#CONF: "


def round_number(number):
    return "{:.5f}".format(float(number))


def supp_to_percent(supp, count):
    return "{:.5f} ({})".format(float(supp) / count, supp)


def process_value(line, token, function, *args, **kwargs):
    """ Find value after given token in line and process this value with given function. """
    if line.find(token) < 0:
        return line.strip()
    value_start_at = line.find(token) + len(token)
    before_value = line[:value_start_at]
    after_value = line[value_start_at:]

    after_parts = after_value.split(' ')
    after_parts = list(map(str.strip, after_parts))
    after_parts[0] = function(after_parts[0], *args, **kwargs)

    return before_value + " ".join(after_parts)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) < 1:
        print("Missing arguments - input file name", file=sys.stderr)
        return -1

    file_name = argv[0]
    token = CONF_TOKEN
    fnc = round_number
    count = None

    if len(argv) >= 2:
        count = float(argv[1])
        token = SUPP_TOKEN
        fnc = supp_to_percent

    for line in fileinput.input(file_name, inplace=1):
        if count is None:
            print(process_value(line, token, fnc))
        else:
            print(process_value(line, token, fnc, count))


if __name__ == '__main__':
    status = main()
    sys.exit(status)
