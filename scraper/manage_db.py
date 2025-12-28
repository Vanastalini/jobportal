import sqlite3
from datetime import datetime

DB_PATH = "D:/major/scraper/jobs.db"

def connect():
    return sqlite3.connect(DB_PATH)

def list_tables():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    print("Tables:", tables)
    conn.close()

def view_users():
    conn = connect()
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM users;")
        users = c.fetchall()
        print("Users:", users)
    except sqlite3.OperationalError:
        print("⚠️ 'users' table does not exist.")
    conn.close()

def clear_users():
    conn = connect()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM preferences;")
        c.execute("DELETE FROM users;")
        conn.commit()
        print("✅ Users and preferences cleared.")
    except sqlite3.OperationalError:
        print("⚠️ Tables do not exist.")
    conn.close()

def add_test_user():
    conn = connect()
    c = conn.cursor()
    try:
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE,
                password TEXT
            );
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                keyword TEXT,
                location TEXT,
                salary TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        """)

    
        c.execute("INSERT OR IGNORE INTO users (name, email, password) VALUES (?, ?, ?);",
                  ("Alice", "alice@example.com", "password123"))
        user_id = c.lastrowid if c.lastrowid else c.execute("SELECT id FROM users WHERE email=?", ("alice@example.com",)).fetchone()[0]


        c.execute("INSERT OR IGNORE INTO preferences (user_id, keyword, location, salary) VALUES (?, ?, ?, ?);",
                  (user_id, "python developer", "chennai", "5-10 LPA"))

        conn.commit()
        print("✅ Test user added with a sample preference.")
    except Exception as e:
        print("❌ Error:", e)
    conn.close()

if __name__ == "__main__":
    print("\n--- DB Management ---\n")
    list_tables()
    view_users()
    add_test_user()
