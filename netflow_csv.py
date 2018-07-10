#!/bin/python3
# Seth Giovanetti

import csv
import glob
import netflow_util as util
import sys


def opencsv(globstr, args):
    data = []
    for filename in glob.glob(globstr):
        print(filename)
        sys.stdout.flush()
        print("Reading file")
        print('[', end='')
        # print("Lines: " + str(sum(1 for line in open(filename))))
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
                if (i % 50000 == 0):
                    print('#', end='')
                    sys.stdout.flush()
        print(']')
        sys.stdout.flush()

        # Conservatively compress data
        print("Compressing file")
        sheet = util.combine_data(sheet, lambda a, b: (
            a['src_ip'] == b['src_ip'] and a['dest_ip'] == b['dest_ip'] and a['flow_dir'] == b['flow_dir']
        ), 'src_ip')
        data += sheet
    # print(data)
    return data
