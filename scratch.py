import pandas as pd
import psutil
import ipdtype as ipf
import numpy as np


def dumpMem():
    fmtstr = "{}M/{}M, {:03.2f}%"
    factor = (2**20)
    for m in [psutil.virtual_memory, psutil.swap_memory]:
        perc = (m().used / m().total) * 100
        print(fmtstr.format(
            int(m().used / factor),
            int(m().total / factor),
            perc
        )
        )


def analyzeDF(df):
    print("------[")
    print("Frame with {} total rows".format(len(df)))
    dumpMem()
    print(df.head())
    print(df.info(memory_usage='deep'))
    for dtype in ['float', 'int', 'object']:
        selected_dtype = df.select_dtypes(include=[dtype])
        mean_usage_b = selected_dtype.memory_usage(deep=True).sum()
        mean_usage_mb = mean_usage_b / 1024 ** 2
        print("Memory usage for {:>6} columns: {:03.2f} MB".format(
            dtype, mean_usage_mb))
    print("]------")


a = analyzeDF

dtypes = {
    '_time': np.uint64,
    'bytes_in': np.float16
}
convs = {
    'dest_ip': ipf.stou,
    'src_ip': ipf.stou
}
cols = ['_time', 'bytes_in', 'dest_ip', 'src_ip']


def getDF(foil):
    return pd.read_csv(
        foil,
        usecols=cols,
        dtype=dtypes,
        converters=convs
    )


def get():
    return getDF("/data/netflow/DF.csv")


def get5():
    return getDF("/data/netflow/DF5.csv")


df = get()
df2 = df.dropna(thresh=0)
df3 = df[~(df['src_ip'] == ipf.bad) & ~(df['dest_ip'] == ipf.bad)]

df5 = get5()

for dfx in [df, df2, df3]:
    a(dfx)
