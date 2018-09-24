from datetime import datetime
import sqlite3

conn = sqlite3.connect("movie.db")
c = conn.cursor()

with open("data_user.txt", "rt") as f:
    for line in f.readlines():
        cmd = line % datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(cmd)
        c.execute(cmd)

conn.commit()
conn.close()

