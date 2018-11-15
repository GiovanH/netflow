import tables


class Flow(tables.IsDescription):
    bytes_in = tables.Int64Col()
    dest_ip = tables.StringCol(16)
    src_ip = tables.StringCol(16)
    linenum = tables.Int32Col()
    time = tables.Int32Col()
    filename = tables.StringCol(128)


h5file = tables.open_file("./jobj/db.h5", mode="w", title="Netflow")
table = h5file.create_table("/", 'flowtable', Flow, "Flows")
print(h5file)

flow = table.row
for i in range(0, 2):
    flow['filename'] = 'Filename: %6d' % (i)
    flow['linenum'] = i
    # Insert a new particle record
    flow.append()
table.flush()

print(h5file)

# table = h5file.root.flowtable
rows = [x[:] for x in table.iterrows()]
print(rows)
