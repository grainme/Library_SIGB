import sqlite3

con = sqlite3.connect("database.db")

cur = con.cursor()

s = cur.execute("PRAGMA foreign_key_list(Exemplaire)")
r = cur.fetchall()
print(r)