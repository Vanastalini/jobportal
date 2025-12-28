import sqlite3
from scraper.indeed_selenium_scraper import scrape_indeed_jobs, save_to_csv, save_to_db

def fetch_user_preferences(db_path="D:/major/scraper/jobs.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT keyword, location FROM preferences")
    prefs = c.fetchall()
    conn.close()
    return prefs

if __name__ == "__main__":
    prefs = fetch_user_preferences()
    print(f"✅ Found {len(prefs)} user preferences")

    all_jobs = []
    for keyword, location in prefs:
        print(f"🔎 Scraping jobs for: {keyword} in {location}")
        jobs = scrape_indeed_jobs(keyword, location, pages=1)  # pages can be >1
        save_to_db(jobs)
        all_jobs.extend(jobs)

    if all_jobs:
        save_to_csv(all_jobs, "D:/major/scraper/auto_jobs.csv")
