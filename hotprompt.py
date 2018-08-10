# "C:/ProgramData/Anaconda3/python.exe" -i  netflow.py \
#     --percent 70 \
#     --nowindow \
#     --verbose \
#     --scaletozero \
#     --regress 1\
#     "../20180110/*0.csv" \
#     c

import netflow
import copy

glob = "../20180110/*.csv"
netflow.init(["--nowindow", glob])

for num in [8, 10, 12, 16]:
    netflow.args.num = num
    netflow.ngraph.graph_icannstacktime(copy.deepcopy(netflow.data), netflow.args.num, '1', "src_ip", overlap=False)
    # o = "_".join(['icannstacktime', 'in', 'src'])
    # print(o)
    # netflow.options[o]()
