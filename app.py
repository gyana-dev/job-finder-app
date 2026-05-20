from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = "b031fa19e3msh9d1756d685e653bp16f1dfjsnd18514090916"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

def fetch_jobs(search_query):

    all_jobs = []

    # Fetch multiple pages dynamically
    for page in range(1, 6):

        url = "https://jsearch.p.rapidapi.com/search"

        querystring = {
            "query": search_query,
            "page": str(page),
            "num_pages": "1"
        }

        response = requests.get(
            url,
            headers=headers,
            params=querystring,
            timeout=30
        )

        if response.status_code == 200:

            data = response.json()

            if "data" in data:

                for item in data["data"]:

                    all_jobs.append({
                        "title": item.get("job_title", "No Title"),
                        "company": item.get("employer_name", "Unknown"),
                        "location": item.get("job_city", "India"),
                        "link": item.get("job_apply_link", "#"),
                        "source": item.get("job_publisher", "JSearch")
                    })

    # Remove duplicates
    unique_jobs = []
    seen = set()

    for job in all_jobs:

        key = (
            job["title"],
            job["company"]
        )

        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    return unique_jobs


@app.route("/", methods=["GET", "POST"])
def home():

    role = ""
    location = ""

    # Default live homepage jobs
    homepage_query = """
    QA Engineer OR
    SDET OR
    Automation Test Engineer OR
    Python Automation Engineer OR
    AI QA Engineer
    """

    jobs = fetch_jobs(homepage_query)

    # User Search
    if request.method == "POST":

        role = request.form.get("role")
        location = request.form.get("location")

        if role and location:
            custom_query = f"{role} jobs in {location}"

        elif role:
            custom_query = f"{role} jobs"

        elif location:
            custom_query = f"jobs in {location}"

        else:
            custom_query = homepage_query

        searched_jobs = fetch_jobs(custom_query)

        # Add searched jobs also
        jobs.extend(searched_jobs)

        # Remove duplicates again
        unique_jobs = []
        seen = set()

        for job in jobs:

            key = (
                job["title"],
                job["company"]
            )

            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)

        jobs = unique_jobs

    return render_template(
        "index.html",
        jobs=jobs,
        role=role,
        location=location
    )


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
