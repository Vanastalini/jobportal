from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import sqlite3
from datetime import datetime
import time

def scrape_indeed_jobs(keyword, location, pages=2, headless=True):
    options = Options()
    options.headless = headless
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    jobs = []

    for page in range(pages):
        url = f"https://www.indeed.com/jobs?q={keyword}&l={location}&start={page*10}"
        print(f"[Page {page+1}] Fetching: {url}")
        driver.get(url)
        time.sleep(3)

        job_cards = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")
        print(f"  Found {len(job_cards)} jobs on page {page+1}")

        for job in job_cards:
            try:
                title = job.find_element(By.CLASS_NAME, "jobTitle").text
            except:
                title = "Not Provided"

            try:
                company = job.find_element(By.CLASS_NAME, "companyName").text
            except:
                company = "Not Provided"

            
            try:
                location_txt = job.find_element(By.CSS_SELECTOR, ".companyLocation, .css-1p0sjhy").text
            except:
                location_txt = "Not Provided"

            
            try:
                salary = job.find_element(By.CSS_SELECTOR, ".salary-snippet-container, .metadata.salary-snippet-container, .salary-snippet").text
            except:
                salary = "Not Provided"

            try:
                snippet = job.find_element(By.CLASS_NAME, "job-snippet").text
            except:
                snippet = "Not Provided"

            try:
                job_url = job.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                job_url = "Not Provided"

            jobs.append({
                "title": title,
                "company": company,
                "location": location_txt,
                "salary": salary,
                "snippet": snippet,
                "url": job_url,
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    driver.quit()
    return jobs


def save_to_csv(jobs, filename="D:/major/scraper/jobs.csv"):
    fieldnames = ["title", "company", "location", "salary", "snippet", "url", "scraped_at"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs)
    print(f"✅ Saved {len(jobs)} jobs to CSV: {filename}")


def save_to_db(jobs, db_path="D:/major/scraper/jobs.db", clear_old=True):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            salary TEXT,
            snippet TEXT,
            url TEXT UNIQUE,
            scraped_at TEXT
        )
    """)
    if clear_old:
        c.execute("DELETE FROM jobs")
        print("🧹 Old job data cleared from database.")
    for job in jobs:
        c.execute("""
            INSERT OR IGNORE INTO jobs (title, company, location, salary, snippet, url, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (job["title"], job["company"], job["location"], job["salary"], job["snippet"], job["url"], job["scraped_at"]))
    conn.commit()
    conn.close()
    print(f"✅ Inserted {len(jobs)} jobs into DB: {db_path}")
