import sqlite3

DB_PATH = "D:/major/scraper/jobs.db"
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS preferences;")
c.execute("""
    CREATE TABLE preferences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        keyword TEXT,
        location TEXT,
        salary TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
""")
print("✅ preferences table recreated with 'salary' column.")
conn.commit()
conn.close()
