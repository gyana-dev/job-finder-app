from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

API_KEY = "b031fa19e3msh9d1756d685e653bp16f1dfjsnd18514090916"

@app.route("/")
def home():

    jobs = []

    try:

        url = "https://jsearch.p.rapidapi.com/search"

        querystring = {
            "query": "QA Automation Engineer jobs in India",
            "page": "1",
            "num_pages": "1"
        }

        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }

        response = requests.get(
            url,
            headers=headers,
            params=querystring,
            timeout=20
        )

        print(response.status_code)
        print(response.text)

        data = response.json()

        if "data" in data:

            for item in data["data"]:

                jobs.append({
                    "title": item.get("job_title", "No Title"),
                    "company": item.get("employer_name", "Unknown"),
                    "location": item.get("job_city", "India"),
                    "link": item.get("job_apply_link", "#"),
                    "source": item.get("job_publisher", "JSearch")
                })

    except Exception as e:
        print("ERROR:", e)

    return render_template("index.html", jobs=jobs)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
