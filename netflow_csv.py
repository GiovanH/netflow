#!/bin/python3
# Seth Giovanetti

import csv
import glob
import netflow_util as util
import sys
import progressbar
from datetime import datetime


def opencsv(globstr, cap):
    data = []
    # print(globstr)
    filenames = glob.glob(globstr)
    # print(filenames)
    for filename in filenames:
        sys.stdout.flush()
        print("Reading file ", filename)
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            totalLines = util.mapcount(filename)
            sheet = []
            i = 1
            bad_rows = 0
            bar = progressbar.ProgressBar(max_value=totalLines, redirect_stdout=True)
            for row in reader:
                try:
                    i += 1
                    row['filename'] = filename
                    row['linenum'] = str(i)
                    row['bytes_in'] = int(row['bytes_in'])
                    row['time'] = datetime.fromtimestamp(int(row['_time'])).hour

                    # Let's only read the fields we're interested in, to save time.
                    sheet.append({field: row[field] for field in ['bytes_in', 'dest_ip', 'src_ip', 'linenum', 'time', 'filename']})
                    if (i == cap):
                        break
                except ValueError as e:
                    # print(e)
                    # print("Row error on file " + filename + " row " + str(i))
                    # print(row)
                    # print("Skipping row")
                    # break
                    bad_rows += 1
                    pass
                bar.update(i)
            bar.finish()
        print(bad_rows, "bad rows in file.")
        sys.stdout.flush()
        sheet = util.multi_combine_data(sheet, ['dest_ip', 'src_ip', 'time', 'filename'])
        data += sheet
    # print(data)
    return data
