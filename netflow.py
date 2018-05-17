#!/bin/python3
#Seth Giovanetti

import argparse
import netflow_csv as ncsv
import traceback
import sys

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,epilog="""
netflow.py
""")

parser.add_argument("files", help="Files to parse (glob)")
parser.add_argument("cmd", nargs='*', help="Command to execute.")

args = parser.parse_args()
print(args)

try:
    data = ncsv.opencsv(args.files)
except:
    print("Error reading files")
    traceback.print_exc(file=sys.stdout)

options = {
    "c" : (lambda: print("C!"))
}

try:
    for c in args.cmd:
        print(c)
        options[c]()
except Exception:
    traceback.print_exc(file=sys.stdout)
