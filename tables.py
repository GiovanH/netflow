class Table(object, header):
    def __init__(self):
        self.rows = []
        self.header = header

    def __getitem__(self, index):
        return rows[index]
