from flask import Flask, render_template, request, redirect, session
import sqlite3
from indeed_selenium_scraper import scrape_indeed_jobs, save_to_csv, save_to_db
from flask import Flask, render_template, request, redirect, session, url_for, flash


app = Flask(__name__)
app.secret_key = "your_secret_key"

DB_PATH = "D:/major/scraper/jobs.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/jobs')
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("D:/major/scraper/jobs.db")
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = c.fetchone()

        if existing_user:
            flash("Email already registered. Please log in.", "error")
            conn.close()
            return redirect(url_for('index'))

        
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                  (name, email, password))
        conn.commit()
        conn.close()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['email'] = user['email']
            return redirect('/jobs')
        else:
            return "⚠️ Invalid credentials!"
    return render_template('login.html')

@app.route('/jobs')
def jobs():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM jobs")  
    jobs_list = c.fetchall()
    conn.close()

    return render_template('jobs.html', jobs=jobs_list)
 
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("index"))

    conn = get_db_connection()
    preferences = conn.execute(
        "SELECT * FROM preferences WHERE user_id = ?", (session["user_id"],)
    ).fetchall()
    conn.close()

    return render_template("dashboard.html", preferences=preferences)
@app.route("/scrape_jobs", methods=["POST"])
def scrape_jobs():
    if "user_id" not in session:
        return redirect(url_for("index"))

    keyword = request.form["keyword"]
    location = request.form["location"]

    
    jobs = scrape_indeed_jobs(keyword, location, pages=1)

    
    save_to_csv(jobs)

    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM jobs WHERE title LIKE ? AND location LIKE ?", (f"%{keyword}%", f"%{location}%"))
    conn.commit()
    conn.close()

    save_to_db(jobs)  
    flash(f"✅ Scraped {len(jobs)} jobs for {keyword} in {location}!", "success")
    return redirect(url_for("jobs"))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
