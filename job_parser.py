import requests
from bs4 import BeautifulSoup


def get_jobs():
    url = "https://www.python.org/jobs/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    job_list = soup.find("ol", class_="list-recent-jobs")
    job_items = job_list.find_all("li") if job_list else []

    keyword = ["python", "django", "backend", "junior", "trainee", "intern"]

    results = []

    for job in job_items[:5]:
        title_tag = job.find("a")
        date_tag = job.find("time")

        if title_tag:
            title = title_tag.text.strip()
            title_lower = title.lower()
            if any(word in title_lower for word in keyword):
                link = "http://www.python.org/jobs/" + title_tag["href"]
                date = date_tag.text.strip() if date_tag else "no data"
                results.append(f"{title}\n{date}\n{link}")

        if len(results) > 5:
            break

    return "\n\n".join(results) if results else "No jobs found 🫠"
