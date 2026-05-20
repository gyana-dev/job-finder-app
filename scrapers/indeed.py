import requests
from bs4 import BeautifulSoup

def fetch_indeed_jobs(role):
    url = f"https://in.indeed.com/jobs?q={role.replace(' ', '+')}&l=Remote"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    cards = soup.find_all("div", class_="job_seen_beacon")

    for card in cards[:15]:
        title_tag = card.find("h2")
        company_tag = card.find("span", class_="companyName")
        location_tag = card.find("div", class_="companyLocation")
        link_tag = card.find("a")

        title = title_tag.text.strip() if title_tag else "No Title"
        company = company_tag.text.strip() if company_tag else "Unknown"
        location = location_tag.text.strip() if location_tag else "Remote"

        link = ""
        if link_tag and link_tag.get("href"):
            link = "https://in.indeed.com" + link_tag.get("href")

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "link": link,
            "source": "Indeed"
        })

    return jobs
