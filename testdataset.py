import sqlite3
conn = sqlite3.connect('jobj/whois.db')

cur = conn.cursor()

cur.execute("PRAGMA foreign_keys = ON")


cur.execute("""
CREATE TABLE IF NOT EXISTS entity(
  name     TEXT
);""")
cur.execute("""
CREATE TABLE IF NOT EXISTS ip(
  addr     TEXT,
  owner	   TEXT,
  UNIQUE(addr)
);
""")

# Save (commit) the changes
conn.commit()

ips = [('192.168.1.1'),
       ('10.10.10.10'),
       ('1.2.3.4')
       ]
for ip in ips:
    # cur.execute('SELECT * FROM entity WHERE name=?', ('local',))
    # index = cur.fetchone()
    index = 'local'
    t = (ip, index,)
    cur.execute('INSERT OR IGNORE INTO ip VALUES (?,?)', t)

conn.commit()

cur.execute('SELECT * FROM ip')
for match in cur:
	print(match)

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
