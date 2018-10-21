import tables
import netflow_util as util


class Flow(tables.IsDescription):
    bytes_in = tables.Int64Col()
    dest_ip = tables.StringCol(16)
    src_ip = tables.StringCol(16)
    linenum = tables.Int32Col()
    time = tables.TimeCol()
    filename = tables.StringCol(128)
    whois_owner_dest_ip = tables.StringCol(64)
    whois_owner_src_ip = tables.StringCol(64)
    flowdir = tables.Int8Col()


flowFields = ['bytes_in', 'dest_ip', 'src_ip', 'linenum', 'time', 'filename']


class H5Manager():

    def __init__(self):
        self.h5file = tables.open_file("./jobj/db.h5", mode="w", title="Netflow")
        self.flowTable = self.h5file.create_table("/", 'flowtable', Flow, "Flows")

    def readFlowRow(self, rowDict):
        flow = self.flowTable.row
        for column in flowFields:
            flow[column] = rowDict[column]
        flow['flowdir'] = util.flowdirOfFlow(rowDict)
        # Insert a new particle record
        flow.append()

    def flush(self):
        self.flowTable.flush()

    def flowWhere(self, criteria):
        table = self.h5file.root.flowtable
        return table.where(criteria)
