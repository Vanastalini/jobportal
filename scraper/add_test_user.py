import sqlite3

DB_PATH = "D:/major/scraper/jobs.db"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()


c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
);
""")


try:
    c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
              ("Alice", "alice@example.com", "password123"))
except sqlite3.IntegrityError:
    pass  

conn.commit()
conn.close()
print("✅ Test user added: alice@example.com / password123")
