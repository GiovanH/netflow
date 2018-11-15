#!/bin/python3
# Seth Giovanetti

import csv
import glob
import netflow_util as util
import sys
import progressbar
from datetime import datetime

import numpy as np
import ipdtype as ipf
import pandas as pd

dtypes = {
    '_time': np.uint32,
    'bytes_in': np.float32
}
convs = {
    'dest_ip': ipf.stou,
    'src_ip': ipf.stou
}
cols = ['_time', 'bytes_in', 'dest_ip', 'src_ip']


def pandaReadToDFChunky(filenames):
    # np.array([int(m) for m in ip.split(".")], dtype=np.uint8)

    chunksize = (8**7)
    # Store a list of dataframes: one dataframe per file
    dfs = []
    with progressbar.ProgressBar(max_value=len(filenames)) as bar:
        i_bar = 0
        for f in filenames:
            for chunk in pd.read_csv(
                f,
                usecols=cols,
                dtype=dtypes,
                converters=convs,
                chunksize=chunksize
            ):
                # Append chunk to list
                dfs.append(chunk)
            i_bar += 1
            bar.update(i_bar)
    df = pd.concat(dfs, ignore_index=True)

    print("### Dropping bad values of type {}".format(ipf.bad))
    df = df[
        (df['src_ip'] != ipf.bad) |
        (df['dest_ip'] != ipf.bad)
    ]
    return df


def loadCsv(globstr):
    print(globstr)
    filenames = glob.glob(globstr)
    DF = pandaReadToDFChunky(filenames)
    # print(filenames)
    return DF
