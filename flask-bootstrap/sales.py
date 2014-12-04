import sqlite3 as lite
import sys

sales = (
    ("John", 19600),
    ("Johnny", 29600),
    ("Jack", 17600),
    ("Dan", 20600),
    ("Kevin", 19400),
    ("James", 20300),
    ("Thomas", 23400),
)
con = lite.connect("sales.db")
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS reps")
    cur.execute("CREATE TABLE reps(rep_name TEXT, amount INT)")
    cur.executemany("INSERT INTO reps VALUES(?, ?)", sales)