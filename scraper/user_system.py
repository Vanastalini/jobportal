import sqlite3

DB_PATH = "D:/major/scraper/jobs.db"
def init_user_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()


    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    
    c.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            keyword TEXT,
            location TEXT,
            salary_range TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    
    c.execute("""
        CREATE TABLE IF NOT EXISTS saved_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            job_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(job_id) REFERENCES jobs(id),
            UNIQUE(user_id, job_id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ User-related tables initialized!")


def register_user(name, email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                  (name, email, password))
        conn.commit()
        print(f"✅ User '{name}' registered successfully!")
    except sqlite3.IntegrityError:
        print("⚠️ Email already registered!")
    finally:
        conn.close()


def login_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT id, name FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()

    if user:
        print(f"✅ Login successful! Welcome {user[1]}")
        return user[0]  
    else:
        print("❌ Invalid email or password.")
        return None


def save_preferences(user_id, keyword, location, salary_range):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("INSERT INTO preferences (user_id, keyword, location, salary_range) VALUES (?, ?, ?, ?)", 
              (user_id, keyword, location, salary_range))
    conn.commit()
    conn.close()
    print("✅ Preferences saved!")


def get_user_preferences(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT keyword, location, salary_range FROM preferences WHERE user_id=?", (user_id,))
    prefs = c.fetchall()
    conn.close()

    return prefs

def save_job_for_user(user_id, job_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        c.execute("INSERT INTO saved_jobs (user_id, job_id) VALUES (?, ?)", (user_id, job_id))
        conn.commit()
        print("✅ Job saved successfully!")
    except sqlite3.IntegrityError:
        print("⚠️ Job already saved!")
    finally:
        conn.close()

if __name__ == "__main__":
    init_user_db()
    register_user("Alice", "alice@example.com", "pass123")
    user_id = login_user("alice@example.com", "pass123")

    if user_id:
        save_preferences(user_id, "python developer", "chennai", "5-10 LPA")

        
        prefs = get_user_preferences(user_id)
        print("📌 Current preferences:", prefs)

        
        save_job_for_user(user_id, 1)
