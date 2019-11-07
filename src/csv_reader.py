#!/usr/bin/env python3

import csv

# This function returns properties props (list)
# found on file fname as a tuple
def get_csv_prop(fname, props):
    o = ()
    try:
        with open(fname) as f:
            r = csv.reader(f, delimiter = ',')
            for el in r:
                for p in props:
                    if el[0] == p:
                        o += (el[1].strip(),)
    except IOError:
        print(f"Error trying to open file at {fname}")
    return o
            
