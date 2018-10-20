#!/bin/python3
# Seth Giovanetti

import csv
import glob
import netflow_util as util
import sys
import progressbar
# import traceback
from datetime import datetime


def loadCsv(globstr, hmgr, cap=-1):
    # print(globstr)
    filenames = glob.glob(globstr)
    # print(filenames)
    for filename in filenames:
        sys.stdout.flush()
        print("Reading file ", filename)
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            totalLines = util.mapcount(filename)
            i = 1
            bad_rows = 0
            bar = progressbar.ProgressBar(max_value=totalLines, redirect_stdout=True)
            for row in reader:
                i += 1
                try:
                    row['filename'] = filename
                    row['linenum'] = str(i)
                    row['time'] = datetime.fromtimestamp(int(row['_time'])).hour

                    # Let's only read the fields we're interested in, to save time.
                    hmgr.readFlowRow(row)
                    if (i == cap):
                        break
                except (ValueError, TypeError) as e:
                    #print(e)
                    #print("Row error on file " + filename + " row " + str(i))
                    #print(row)
                    # print("Skipping row")
                    # traceback.print_exc()
                    # break
                    bad_rows += 1
                    pass
                bar.update(i)
            bar.finish()
        print(bad_rows, "bad rows in file.")
        sys.stdout.flush()
