from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = "b031fa19e3msh9d1756d685e653bp16f1dfjsnd18514090916"

@app.route("/", methods=["GET", "POST"])
def home():

    jobs = []

    # Default search values
    role = "QA Engineer"
    location = "India"

    # User search
    if request.method == "POST":
        role = request.form.get("role")
        location = request.form.get("location")

    try:

        url = "https://jsearch.p.rapidapi.com/search"

        query = f"{role} jobs in {location}"

        querystring = {
            "query": query,
            "page": "1",
            "num_pages": "5"
        }

        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }

        response = requests.get(
            url,
            headers=headers,
            params=querystring,
            timeout=30
        )

        data = response.json()

        if "data" in data:

            for item in data["data"]:

                jobs.append({
                    "title": item.get("job_title", "No Title"),
                    "company": item.get("employer_name", "Unknown Company"),
                    "location": item.get("job_city", "India"),
                    "link": item.get("job_apply_link", "#"),
                    "source": item.get("job_publisher", "JSearch")
                })

    except Exception as e:
        print("ERROR:", e)

    return render_template(
        "index.html",
        jobs=jobs,
        role=role,
        location=location
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
