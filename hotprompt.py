# "C:/ProgramData/Anaconda3/python.exe" -i  netflow.py \
#     --percent 70 \
#     --nowindow \
#     --verbose \
#     --scaletozero \
#     --regress 1\
#     "../20180110/*0.csv" \
#     c

import netflow_h5 as h5
import netflow_csv as ncsv
import time
import pandas as pd
import glob

globs = "/data/netflow/*test.csv"

def benchmark(f, runs):
    stopwatch = []
    for i in range(0, runs):
        print("Running run {0}".format(i))
        start = time.time()

        f()

        end = time.time()
        elapsed = end - start
        stopwatch.append(elapsed)

    for i in range(0,runs):
        print("Run {1} Time elapsed: '{0}'".format(stopwatch[i], i))

    print("Average: {0}".format(sum([float(t) for t in stopwatch])))

def vanilla():
    with h5.H5Manager() as hmgr:
        ncsv.loadCsv(globs, hmgr)

def pandaEach():
    for f in glob.glob(globs):
        p = pd.read_csv(f, usecols=h5.flowFields)
        for row in p:
            hmgr.readFlowRow(row)

benchmark(pandaEach, 3)
benchmark(vanilla, 3)
# glob = "../20180110/*.csv"
# netflow.init(["--nowindow", glob])

# for num in [8, 10, 12, 16]:
#     netflow.args.num = num
#     netflow.ngraph.graph_icannstacktime(copy.deepcopy(netflow.data), netflow.args.num, '1', "src_ip", overlap=False)
    # o = "_".join(['icannstacktime', 'in', 'src'])
    # print(o)
    # netflow.options[o]()
