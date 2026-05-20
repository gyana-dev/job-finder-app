import requests
from bs4 import BeautifulSoup

def fetch_naukri_jobs(role):
    url = f"https://www.naukri.com/{role.replace(' ', '-')}-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for item in soup.find_all("article")[:10]:
        title = item.get_text(strip=True)[:100]
        jobs.append({
            "title": title,
            "source": "Naukri"
        })

    return jobs