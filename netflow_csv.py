#!/bin/python3
# Seth Giovanetti

import csv
import glob
import netflow_util as util
import sys


def opencsv(globstr, cap):
    data = []
    # print(globstr)
    filenames = glob.glob(globstr)
    # print(filenames)
    for filename in filenames:
        print(filename)
        sys.stdout.flush()
        print("Reading file")
        print('[', end='')
        # print("Lines: " + str(sum(1 for line in open(filename))))
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            sheet = []
            i = 1
            for row in reader:
                try:
                    i += 1
                    row['filename'] = filename
                    row['linenum'] = str(i)
                    row['bytes_in'] = int(row['bytes_in'])
                    row['time'] = row['_time'][11:13]

                    # Let's only read the fields we're interested in, to save time.
                    sheet.append({field: row[field] for field in ['bytes_in', 'dest_ip', 'flow_dir', 'src_ip', 'linenum', 'time', 'filename']})
                    if (i == cap):
                        break
                    if (i % 50000 == 0):
                        print('#', end='')
                        sys.stdout.flush()
                except ValueError:
                    # print("Row error on file " + filename + " row " + str(i))
                    # print(row)
                    # print("Skipping row.")
                    # break
                    pass
        print(']')
        sys.stdout.flush()
        sheet = util.multi_combine_data(sheet, ['dest_ip', 'flow_dir', 'src_ip', 'time', 'filename'])
        data += sheet
    # print(data)
    return data
