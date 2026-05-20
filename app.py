from flask import Flask, render_template
from scrapers.naukri import fetch_naukri_jobs
from scrapers.indeed import fetch_indeed_jobs
import os

app = Flask(__name__)

@app.route('/')
def home():

    jobs = []

    # Try fetching Indeed jobs
    try:
        indeed_jobs = fetch_indeed_jobs("software engineer")
        jobs.extend(indeed_jobs)
    except Exception as e:
        print("Indeed Error:", e)

    # Try fetching Naukri jobs
    try:
        naukri_jobs = fetch_naukri_jobs("software engineer")
        jobs.extend(naukri_jobs)
    except Exception as e:
        print("Naukri Error:", e)

    # Fallback demo jobs if scraping fails
    if len(jobs) == 0:
        jobs = [
            {
                "title": "AI QA Engineer",
                "company": "Google",
                "location": "Remote",
                "link": "https://careers.google.com",
                "source": "Demo"
            },
            {
                "title": "Software Test Engineer",
                "company": "Infosys",
                "location": "Bangalore",
                "link": "https://www.infosys.com/careers",
                "source": "Demo"
            },
            {
                "title": "Automation QA Engineer",
                "company": "TCS",
                "location": "Hyderabad",
                "link": "https://www.tcs.com/careers",
                "source": "Demo"
            }
        ]

    # Remove duplicates
    unique_jobs = []
    seen = set()

    for job in jobs:
        key = (job['title'], job['company'])

        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    return render_template("index.html", jobs=unique_jobs)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
