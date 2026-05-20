import requests
from bs4 import BeautifulSoup

def fetch_naukri_jobs(role):

    url = f"https://www.naukri.com/{role.replace(' ', '-')}-jobs"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    jobs = []

    if response.status_code != 200:
        return jobs

    soup = BeautifulSoup(response.text, "html.parser")

    cards = soup.find_all("article", class_="jobTuple")

    for card in cards[:15]:

        title_tag = card.find("a", class_="title")
        company_tag = card.find("a", class_="subTitle")
        location_tag = card.find("span", class_="locWdth")

        title = title_tag.text.strip() if title_tag else "No Title"
        company = company_tag.text.strip() if company_tag else "Unknown"
        location = location_tag.text.strip() if location_tag else "India"

        link = ""
        if title_tag and title_tag.get("href"):
            link = title_tag.get("href")

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "link": link,
            "source": "Naukri"
        })

    return jobs
