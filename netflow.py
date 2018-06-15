#!/bin/python3
#Seth Giovanetti

import argparse
import traceback
import sys

import netflow_csv as ncsv
import netflow_graphing as ngraph

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,epilog="""
netflow.py
""")

parser.add_argument("files", help="Files to parse (glob)")
parser.add_argument('--reset','-r', action='store_true')
parser.add_argument('--cap', type=int, default=-1, help='Maximum entries to process')
parser.add_argument('--num', type=int, default=20, help='Top N entries, if applicable')
parser.add_argument('--field', type=str, default='bytes_in', help='Field of interest, if applicable')
parser.add_argument('--percent', type=float, default=20, help='Percent, if applicable')
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

options = {
    "dump" : (lambda: dump(data)),
    "oniondump" : (lambda: oniondump(data)),
    "hist_out" : (lambda: ngraph.top_contributors_noncum(data, args.num,'0')),
    "hist_in" : (lambda: ngraph.top_contributors_noncum(data, args.num,'1')),
    "top_contributors_out" : (lambda: ngraph.top_contributors(data, args.num,'0')),
    "top_contributors_in" : (lambda: ngraph.top_contributors(data, args.num,'1')),
    "top_percent_in" : (lambda: ngraph.top_contributors_percent(data, args.percent,'1')),
    "top_percent_out" : (lambda: ngraph.top_contributors_percent(data, args.percent,'0')),
    "c" : (lambda: print("C!"))
}

try:
    for c in args.cmds:
        print(c)
        options[c]()
except KeyError:
    print("No such command " + c)
    print("Valid commands are:")
    print(", ".join(key for key in options.keys()))
