from cs50 import SQL

db = SQL("sqlite:///database.db")
s = db.execute("SELECT id_bitc FROM bibliothecaire")


# Creating a list of all the values in the dictionary.
L=[]
for i in db.execute("SELECT id_bitc FROM bibliothecaire"):
    L.append(*iter(i.values()))
print(L)

import sqlite3


db = sqlite3.connect("database.db")

cur = db.cursor()

res = cur.execute("SELECT id_bitc FROM bibliothecaire")
for i in res.fetchall():
    print(i[0])