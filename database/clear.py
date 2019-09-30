import sqlite3
conn = sqlite3.connect('Benchmark.db')

c = conn.cursor()

c.execute("DELETE FROM bids")
c.execute("DELETE FROM listing")
c.execute("DELETE FROM metadata")
c.execute("DELETE FROM purchase")
c.execute("DELETE FROM user")
c.execute("UPDATE sqlite_sequence SET seq=0")

conn.commit()

conn.close()