#!/bin/python3
# Seth Giovanetti

import csv
import glob
import netflow_util as util
import sys


def opencsv(globstr, cap):
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
            i = 1
            for row in reader:
                i += 1
                row['filename'] = filename
                row['linenum'] = str(i)
                row['time'] = row['_time'][11:15]
                # sheet.append(dict(row))
                # Let's only read the fields we're interested in, to save time.
                sheet.append({field: row[field] for field in ['bytes_in', 'dest_ip', 'flow_dir', 'src_ip', 'linenum', 'time', 'filename']})
                # if row['src_ip'] == "10.189.40.74" and row['dest_ip'] == "10.100.12.41":
                #     print(i)
                #     print(row)
                cap -= 1
                if (cap == 0):
                    break
                if (i % 50000 == 0):
                    print('#', end='')
                    sys.stdout.flush()
        print(']')
        sys.stdout.flush()

        # Conservatively compress data
        print("Consolidating file records")
        sys.stdout.flush()
        sheet = util.combine_data(sheet, lambda a, b: (
            a['flow_dir'] == b['flow_dir'] and a['src_ip'] == b['src_ip'] and a['dest_ip'] == b['dest_ip']
        ), 'src_ip')
        data += sheet
    # print(data)
    return data
