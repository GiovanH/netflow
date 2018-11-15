# "C:/ProgramData/Anaconda3/python.exe" -i  netflow.py \
#     --percent 70 \
#     --nowindow \
#     --verbose \
#     --scaletozero \
#     --regress 1\
#     "../20180110/*0.csv" \
#     c

# import netflow_h5 as h5
# import netflow_csv as ncsv
import time
import pandas as pd
import glob
import os
import numpy as np
import psutil

import ipdtype as ipf

# globs = "/data/netflow/NetflowOut_2018-10-31_*.csv"
# globs = "/data/netflow/TestNetflowOut*.csv"
globs = "G:/Stash/Netflow/*.csv"
# globs = "G:/Stash/Netflow/NetflowOut_2018-11-11_00-05-00.csv"
# print(globs)


def dumpMem():
    fmtstr = "{}M/{}M, {:03.2f}%"
    factor = (2**20)
    totalMemPerc = 0
    totalMemThreshhold = 160
    for m in [psutil.virtual_memory, psutil.swap_memory]:
        perc = (m().used / m().total) * 100
        print(fmtstr.format(
            int(m().used / factor),
            int(m().total / factor),
            perc
        )
        )
        totalMemPerc += perc
        # print("{:0.0f}/{}".format(totalMemPerc, totalMemThreshhold))
    if totalMemPerc > totalMemThreshhold:
        print("BREAKER TRIP")
        # Trip the breaker
        import sys
        sys.exit()


benchmarks = []


def benchmark(f, runs, label):
    print("Benchmarking method: \"{}\"".format(label))
    stopwatch = []
    for i in range(0, runs):
        print("Running run {0}".format(i + 1))
        start = time.time()

        f()

        end = time.time()
        elapsed = end - start
        stopwatch.append(elapsed)
        print("Run {1} Time elapsed: '{0}'".format(stopwatch[i], i + 1))

    print("Benchmarked method: \"{}\"".format(label))
    for i in range(0, runs):
        print("Run {1} Time elapsed: '{0}'".format(stopwatch[i], i + 1))

    total = sum([float(t) for t in stopwatch])
    average = total / runs
    print("Average: {:03.2f}".format(average))
    print("Total: {:03.2f}".format(total))
    global benchmarks
    benchmarks.append([label, stopwatch, average])


def analyzeDF(df):
    dumpMem()
    print("[---------------------------------]")
    print("Frame with {} total rows".format(len(df)))
    # print(df.head())
    print(df.dtypes)
    # print(df.info(memory_usage='deep'))
    for dtype in set(df.dtypes.values):
        selected_dtype = df.select_dtypes(include=[dtype])
        mean_usage_b = selected_dtype.memory_usage(deep=True).sum()
        mean_usage_mb = mean_usage_b / 1024 ** 2
        print("Memory usage for {:>7} columns: {:03.2f} MB".format(
            dtype.name, mean_usage_mb))
    print("[---------------------------------]")


def finalizeList(dfs):
    # print("### Joining")
    df = pd.concat(dfs, ignore_index=True)
    analyzeDF(df)

    print("### Dropping bad values of type {}".format(ipf.bad))
    df = df[
        (df['src_ip'] != ipf.bad) |
        (df['dest_ip'] != ipf.bad)
    ]
    analyzeDF(df)
    return

    # print("### Dropping NA values")
    # df.dropna(thresh=0, inplace=True)
    # analyzeDF(df)


# 2018-10-25: 4 mins per 3 gb
def pandaReadToHDF():
    try:
        os.remove("benchmark.h5")
    except FileNotFoundError:
        pass

    print("Saving HDF")
    for file in glob.glob(globs):
        chunk = pd.read_csv(
            file,
            usecols=cols,
            dtype=dtypes,
            converters=convs
        )
        chunk.to_hdf('benchmark.h5', 'flowtable', append=True)
    # print(df2)


def pandaReadFromHDF():
    print("Reading HDF")
    df2 = pd.read_hdf('benchmark.h5', 'flowtable')
    dumpMem()
    df2.head()


dtypes = {
    '_time': np.uint32,
    'bytes_in': np.float32
}
convs = {
    'dest_ip': ipf.stou,
    'src_ip': ipf.stou
}
cols = ['_time', 'bytes_in', 'dest_ip', 'src_ip']


def pandaReadToDF():
    # Store a list of dataframes: one dataframe per file
    dfs = []

    for file in glob.glob(globs):
        chunk = pd.read_csv(
            file,
            usecols=cols,
            dtype=dtypes,
            converters=convs
        )
        dfs.append(chunk)

    finalizeList(dfs)


def pandaReadToDFSmallFloat():
    # np.array([int(m) for m in ip.split(".")], dtype=np.uint8)
    dtypes = {
        'bytes_in': np.float16,
        '_time': np.uint64
    }
    # Store a list of dataframes: one dataframe per file
    dfs = []

    for file in glob.glob(globs):
        chunk = pd.read_csv(
            file,
            usecols=cols,
            dtype=dtypes,
            converters=convs
        )
        dfs.append(chunk)

    finalizeList(dfs)


def pandaReadToDFChunky():
    # np.array([int(m) for m in ip.split(".")], dtype=np.uint8)

    chunksize = (8**7)
    # Store a list of dataframes: one dataframe per file
    # dfs = []
    # for f in glob.glob(globs):
    #     for chunk in pd.read_csv(
    #         f,
    #         usecols=cols,
    #         dtype=dtypes,
    #         converters=convs,
    #         chunksize=chunksize
    #     ):
    #         # Append chunk to list
    #         dfs.append(chunk)

    dfs = \
        [
            inner for outer in
            [
                chunk for chunk in
                [
                    pd.read_csv(
                        f,
                        usecols=cols,
                        dtype=dtypes,
                        converters=convs,
                        chunksize=chunksize
                    )
                    for f in glob.glob(globs)
                ]
            ]
            for inner in outer
        ]

    # ...that might be worse, actually. geez.
    return finalizeList(dfs)


def pandaReadToDFDropDuring():
    # np.array([int(m) for m in ip.split(".")], dtype=np.uint8)

    # Store a list of dataframes: one dataframe per file
    dfs = []

    for f in glob.glob(globs):
        chunk = pd.read_csv(
            f,
            usecols=cols,
            dtype=dtypes,
            converters=convs
        )
        # print("### Dropping bad values of type {}".format(ipf.bad))
        chunk = chunk[
            (chunk['src_ip'] != ipf.bad) |
            (chunk['dest_ip'] != ipf.bad)
        ]
        # Append chunk to list
        dfs.append(chunk)

    return finalizeList(dfs)


def pandaReadToDFThreaded():

    # np.array([int(m) for m in ip.split(".")], dtype=np.uint8)

    def task(f):
        chunk = pd.read_csv(
            f,
            usecols=cols,
            dtype=dtypes,
            converters=convs
        )
        # Append chunk to list
        return chunk

    import threader
    dfs = threader.map(task, glob.glob(globs))

    return finalizeList(dfs)


def pandaReadToDFABTestA():
    # np.array([int(m) for m in ip.split(".")], dtype=np.uint8)

    # Store a list of dataframes: one dataframe per file
    dfs = []

    for f in glob.glob(globs):
        chunk = pd.read_csv(
            f,
            # engine='c',
            usecols=cols,
            dtype=dtypes
            # parse_dates=False,
            # compression=None,
            # converters=convs
        )
        # Append chunk to list
        dfs.append(chunk)

    return finalizeList(dfs)


def pandaReadToDFABTestB():
    # np.array([int(m) for m in ip.split(".")], dtype=np.uint8)

    # Store a list of dataframes: one dataframe per file
    dfs = []

    for f in glob.glob(globs):
        chunk = pd.read_csv(
            f,
            # engine='python',
            usecols=cols,
            converters=convs,
            dtype=dtypes
            # parse_dates=False,
            # compression=None,
        )
        # Append chunk to list
        dfs.append(chunk)

    return finalizeList(dfs)


# benchmark(pandaEach, 3, "pandaEach (iter)")
runs = 1

# benchmark(ipf.tests, runs, "iptests")
# benchmark(pandaReadToDF, runs, "Plain")
benchmark(pandaReadToDFChunky, runs, "Chunked")
# benchmark(pandaReadToDFSmallFloat, runs, "Small float")
# benchmark(pandaReadToDFThreaded, runs, "Threaded")
# benchmark(pandaReadToHDF, runs, "pandaReadToHDF")
# benchmark(pandaReadToDFDropDuring, runs, "Drop During")
# benchmark(pandaReadToHDF, runs, "pandaReadToHDF")

# benchmark(pandaReadToDFABTestA, runs, "NoConv")
# benchmark(pandaReadToDFABTestB, runs, "Standard")
# benchmark(pandaReadFromHDF, runs, "pandaReadFromHDF")

print("Summary:")
for mark in benchmarks:
    print("{}: average [{:03.2f}]".format(mark[0], mark[2]))
