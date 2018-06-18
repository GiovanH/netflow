#!/bin/python3
#Seth Giovanetti

import csv
import glob
import netflow_util as util
import sys

def opencsv(globstr, args):
    data = []
    for filename in glob.glob(globstr):
        print(filename)
        sys.stdout.flush()
        print('[', end='')
        #print("Lines: " + str(sum(1 for line in open(filename))))
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            sheet = []
            i = 0
            for row in reader:
                row['filename'] = filename
                sheet.append(dict(row))
                i += 1
                args.cap -= 1
                if (args.cap == 0):
                   break
                if (i%50000 == 0):
                    print('#', end='')
                    sys.stdout.flush()
        print(']')
        #util.pickleSave(sheet, filename)
        if args.compress_field is not None:
            sheet = util.combine_data(sheet, lambda a,b: a[args.compress_field]==b[args.compress_field], args.compress_field)
        if args.compress_size is not None:
            for record in sheet:
                record['bytes_in'] = int(record['bytes_in'])/args.compress_size
        data += sheet
    #print(data)
    return data
