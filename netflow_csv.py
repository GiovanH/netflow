#!/bin/python3
#Seth Giovanetti

import csv
import glob
import netflow_util as util

def opencsv(globstr):
    data = []
    for filename in glob.glob(globstr):
        print(filename)
        try:
            sheet = util.pickleLoad(filename)
            data.append(sheet)
            print("Using cached data for file " + filename)
        except:
            print("No cached data, building...")
            with open(filename) as csvfile:
                reader = csv.DictReader(csvfile)
                sheet = []
                for row in reader:
                    row['filename'] = filename
                    sheet.append(row)
            util.pickleSave(sheet, filename)
            data.append(sheet)
    print(data)
    return data
