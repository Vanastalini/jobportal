import sqlite3
from tabulate import tabulate  

db_path = "D:/major/scraper/jobs.db"  

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("SELECT id, title, company, location, salary, url, scraped_at FROM jobs")
rows = cur.fetchall()

print(tabulate(rows, headers=["ID", "Title", "Company", "Location", "Salary", "URL", "Scraped At"], tablefmt="grid"))

conn.close()
