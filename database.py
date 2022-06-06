import sqlite3

conn = sqlite3.connect("healthberry.db")
c = conn.cursor()
c.execute(
    "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT NOT NULL UNIQUE, password TEXT NOT NULL)"
)
conn.commit()
c.close()
