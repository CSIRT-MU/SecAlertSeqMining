#!/bin/bash

# Run with file name containing generated patterns as argument.
# In out.txt file will be saved patterns sorted by support value and in more readable format.
# There can be passed number of transactions in input database as second argument for calculating support as percentage.


# Translate items in patterns to strings
python3 decoder.py

# Sort patterns by support
sort -k 2 -t : -g -r $1 > out.txt

# Calculate support value as percentage if second argument is present
if [ ! -z "$2" ]; then
        python3 process_supp_conf.py out.txt $2
fi

python3 embellish.py out.txt