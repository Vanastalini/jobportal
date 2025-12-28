import sqlite3

DB_PATH = "D:/major/scraper/jobs.db"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()


c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", c.fetchall())


try:
    c.execute("SELECT * FROM users;")
    users = c.fetchall()
    print("Users:", users)
except sqlite3.OperationalError:
    print("⚠️ 'users' table does not exist.")

conn.close()
