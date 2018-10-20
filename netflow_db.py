import sqlite3


class DBManager():

    def __init__(self):
        self.conn = sqlite3.connect('jobj/whois.db')
        self.cur = self.conn.cursor()
        self.initdb()

    def initdb(self):
        self.cur.execute("PRAGMA foreign_keys = ON")
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS entity(
          name     TEXT
        );""")
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS ip(
          addr     TEXT,
          owner    TEXT,
          UNIQUE(addr)
        );
        """)
        # Save (commit) the changes
        self.conn.commit()

    def pushPair(self, ip, owner):
        self.cur.execute('INSERT OR IGNORE INTO ip VALUES (?,?)', (ip, owner,))
        self.conn.commit()
        return owner

    def getOwner(self, ip):
        self.cur.execute('SELECT * FROM ip WHERE addr=?', (ip,))
        first = self.cur.fetchone()
        if first is None:
            return None
        else:
            return first[1]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()


# with DBManager() as db:
#     db.pushPair('Key1', 'Value1')
#     print(db.getOwner('Key1'))
#     print(db.getOwner('Key1'))
#     print(db.getOwner('Key2'))
