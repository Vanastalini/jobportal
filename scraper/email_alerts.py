import sqlite3
import yagmail
from datetime import datetime, timedelta

EMAIL_ADDRESS = "your_email@gmail.com"     
EMAIL_PASSWORD = "your_app_password"        
DB_PATH = "D:/major/scraper/jobs.db"        

def send_email(to_email, subject, body):
    yag = yagmail.SMTP(EMAIL_ADDRESS, EMAIL_PASSWORD)
    yag.send(to=to_email, subject=subject, contents=body)
    print(f"✅ Email sent to {to_email}")


def notify_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()


    c.execute("""
        SELECT u.email, p.keyword, p.location
        FROM users u
        JOIN preferences p ON u.id = p.user_id
    """)
    users = c.fetchall()

    now = datetime.now()
    one_day_ago = now - timedelta(days=1)

    for email, keyword, location in users:
        
        c.execute("""
            SELECT title, company, location, salary, snippet, url, scraped_at
            FROM jobs
            WHERE title LIKE ? COLLATE NOCASE
              AND location LIKE '%' || ? || '%' COLLATE NOCASE
              AND datetime(scraped_at) >= ?
        """, (f"%{keyword}%", f"{location}", one_day_ago.strftime("%Y-%m-%d %H:%M:%S")))

        new_jobs = c.fetchall()
        if new_jobs:
            body = f"Hi!\n\nHere are the new '{keyword}' jobs in {location}:\n\n"
            for job in new_jobs:
                title, company, loc, salary, snippet, url, scraped_at = job
                body += f"- {title} at {company}\n  Location: {loc}\n  Salary: {salary}\n  URL: {url}\n\n"
            body += "Best,\nYour Tech Job Portal"
            send_email(email, f"New {keyword} Jobs in {location}", body)
        else:
            print(f"⚠️ No new jobs for {email} ({keyword} in {location})")

    conn.close()

if __name__ == "__main__":
    notify_users()
