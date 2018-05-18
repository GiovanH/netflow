#!/bin/python3
#Seth Giovanetti

import argparse
import traceback
import sys

import netflow_csv as ncsv

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,epilog="""
netflow.py
""")

parser.add_argument("files", help="Files to parse (glob)")
parser.add_argument('--reset','-r', action='store_true')
parser.add_argument('--cap', type=int, default=-1, help='Maximum entries to process')
parser.add_argument('--field', type=str, default='bytes_in', help='Field of interest')
parser.add_argument("cmds", nargs='*', help="Commands to execute in sequence.")

args = parser.parse_args()

#Hack: Fix cygwin paths
args.files = args.files.replace("/","\\")

#Init data store
data = []

#Get data from cache or csv
try:
    data = ncsv.opencsv(args.files, args)
except:
    print("Error reading files")
    traceback.print_exc(file=sys.stdout)

def dump(data):
    print(data)

def oniondump(data):
    for s in data:
        for r in s:
            print(r)

def histo(data, field):
    import numpy as np
    import matplotlib.pyplot as plt
    graphdata = []
    try:
        graphdata = [point[field] for sheet in data for point in sheet]
    except KeyError:
        print("No such field \"" + field + "\"")
        print("Valid fields:")
        print(', '.join([i for i in data[0][0].keys()]))
        return
    n, bins, patches = plt.hist(graphdata, 50, density=True, facecolor='g', alpha=0.75)
    plt.xlabel(field)
    plt.ylabel('Probability')
    plt.title('Histogram of ' + field)
    plt.grid(True)
    plt.show()

options = {
    "dump" : (lambda: dump(data)),
    "oniondump" : (lambda: oniondump(data)),
    "plot" : (lambda: histo(data, args.field)),
    "c" : (lambda: print("C!"))
}

try:
    for c in args.cmds:
        print(c)
        options[c]()
except Exception:
    traceback.print_exc(file=sys.stdout)
