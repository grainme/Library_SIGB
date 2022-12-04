import sqlite3

def dbcon():
    return sqlite3.connect("database.db")