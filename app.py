from flask import Flask, render_template
from scrapers.naukri import fetch_naukri_jobs
from scrapers.indeed import fetch_indeed_jobs
import os

app = Flask(__name__)

@app.route('/')
def home():

    jobs = []

    # Fetch Naukri Jobs
    try:
        naukri_jobs = fetch_naukri_jobs("qa automation engineer")
        jobs.extend(naukri_jobs)
    except Exception as e:
        print("Naukri Error:", e)

    # Fetch Indeed Jobs
    try:
        indeed_jobs = fetch_indeed_jobs("AI QA Engineer")
        jobs.extend(indeed_jobs)
    except Exception as e:
        print("Indeed Error:", e)

    # Remove duplicate jobs
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
