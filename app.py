from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

API_KEY = "b031fa19e3msh9d1756d685e653bp16f1dfjsnd18514090916"

@app.route('/')
def home():

    url = "https://jsearch.p.rapidapi.com/search-v2"

    querystring = {
        "query": "QA Automation Engineer jobs in India",
        "num_pages": "1",
        "country": "in",
        "date_posted": "all"
    }

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    jobs = []

    if response.status_code == 200:

        data = response.json()

        for item in data.get("data", []):

            jobs.append({
                "title": item.get("job_title", "No Title"),
                "company": item.get("employer_name", "Unknown"),
                "location": item.get("job_city", "India"),
                "link": item.get("job_apply_link", "#"),
                "source": item.get("job_publisher", "JSearch")
            })

    return render_template("index.html", jobs=jobs)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
