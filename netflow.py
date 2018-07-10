#!/bin/python3
# Seth Giovanetti

import argparse

import traceback
import sys
import netflow_csv as ncsv
import netflow_graphing as ngraph
import netflow_util as util
import copy

options = {
    "dump": (
        lambda: dump(
            copy.deepcopy(data)
        )
    ),
    "dumpargs": (
        lambda: print(",".join([l + "=" + util.sluggify(str(vars(args)[l])) for l in vars(args)]))
    ),
    "oniondump": (lambda: oniondump(copy.deepcopy(data))),
    "c": (lambda: print("C!"))
}

for f in [{'value': '1', 'name': 'in'}, {'value': '0', 'name': 'out'}]:
    for ip in ['src', 'dest']:
        options["_".join(["hist", f['name'], ip])] = (
            lambda: ngraph.graph_hist(copy.deepcopy(data), args.num, f['value'], ip + '_ip')
        )
        options["_".join(["top", f['name'], ip])] = (
            lambda: ngraph.graph_top(copy.deepcopy(data), args.num, f['value'], ip + '_ip')
        )
        options["_".join(["top_contributors", f['name'], ip])] = (
            lambda: ngraph.graph_ippercent(copy.deepcopy(data), args.percent, f['value'], ip + '_ip')
        )
        options["_".join(["top_owners", f['name'], ip])] = (
            lambda: ngraph.graph_icannpercent(copy.deepcopy(data), args.percent, f['value'], ip + '_ip')
        )

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 epilog="Valid command values for cmd: \n" + "\n    ".join(key for key in options.keys()))

parser.add_argument("files", help="Files to parse (glob)")
parser.add_argument('--verbose', action='store_true', help='Verbose output for graphing data')

parser.add_argument('--cap', type=int, default=-1,
                    help='Maximum individual entries to process. Used by the CSV parser.')
parser.add_argument('--regress', '-r', action='store_true',
                    help='Attempt linear regression on the output graph.')
parser.add_argument('--nowhois', action='store_true',
                    help='Do not run whois lookup on IP addresses.')
parser.add_argument('--nowindow', action='store_true',
                    help='Do not open the GUI window to display the graph, only save it.')
parser.add_argument('--scaletozero', action='store_true',
                    help='Start the Y axis at zero instead of starting it at the lowest value.')

parser.add_argument('--num', type=int, default=20,
                    help='How many results to show for integer-based caps')
parser.add_argument('--percent', type=float, default=20,
                    help='How many results to show for percentage-based caps')
parser.add_argument('--field', type=str, default='bytes_in',
                    help='Field of interest, if applicable. Default is bytes_in, can be set to bytes_out.')

parser.add_argument('--compress_field', type=str, default=None,
                    help='Compress data by field. Defaults to ip_type. Massive reduction to memory overhead.')
parser.add_argument('--compress_size', type=int, default=1000000,
                    help='Compress byte values by size. Defaults to 1000000 (Megabytes)')  # Compress to MB
parser.add_argument("cmds", nargs='*', help="Commands to execute in sequence.")

# TODO: ARgument, "verbose"

args = parser.parse_args()


ngraph.global_args = args

# Hack: Fix cygwin paths
args.files = args.files.replace("/", "\\")

# Init data store
data = []

# Read data in from CSV files.
# Data is based on a file glob to CSV files that are expected to be netflow exports.
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


try:
    for c in args.cmds:
        print('####################################')
        print('###    ' + c)
        print('####################################')
        options[c]()
except KeyError:
    print("No such command " + c)
    print("Valid commands are:")
    print(", ".join(key for key in options.keys()))
