# "C:/ProgramData/Anaconda3/python.exe" -i  netflow.py \
#     --percent 70 \
#     --nowindow \
#     --verbose \
#     --scaletozero \
#     --regress 1\
#     "../20180110/*0.csv" \
#     c

import netflow_h5 as h5
import pandas as pd
import glob
import numpy as np

globs = "/data/netflow/*test.csv"

def read():
    dtypes = {'_time': np.int32, 'dest_ip': str, 'src_ip': str}
    return pd.concat(
        [pd.read_csv(f, usecols=h5.csvFields, 
            error_bad_lines=False,
            dtype=dtypes) for f in glob.glob(globs)]
        )

dataFrame = read()
print(dataFrame)
print(dataFrame.dtypes)