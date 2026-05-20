import requests
from bs4 import BeautifulSoup

def fetch_indeed_jobs(role):
    url = f"https://in.indeed.com/jobs?q={role.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for item in soup.find_all("a")[:10]:
        title = item.get_text(strip=True)
        if title:
            jobs.append({
                "title": title,
                "source": "Indeed"
            })

    return jobs