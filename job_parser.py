import logging
import requests
from bs4 import BeautifulSoup


def get_jobs():
    url = "https://www.python.org/jobs/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"🌐 Error fetching jobs from Python.org: {e}")
        return "❗ Failed to fetch job listings from python.org"

    try:
        soup = BeautifulSoup(response.text, "html.parser")
        job_list = soup.find("ol", class_="list-recent-jobs")
        job_items = job_list.find_all("li") if job_list else []
    except Exception as e:
        logging.error(f"🧠 Parsing error: {e}")
        return "❗ Error parsing the job listings."

    keyword = ["python", "django", "backend", "junior", "trainee", "intern"]
    results = []

    try:
        for job in job_items[:5]:
            title_tag = job.find("a")
            date_tag = job.find("time")

            if title_tag:
                title = title_tag.text.strip()
                title_lower = title.lower()
                if any(word in title_lower for word in keyword):
                    link = "https://www.python.org/jobs/" + title_tag["href"]
                    date = date_tag.text.strip() if date_tag else "no data"
                    results.append(f"{title}\n{date}\n{link}")

            if len(results) > 5:
                break
    except Exception as e:
        logging.error(f"🔁 Error while processing job items: {e}")
        return "❗ Something went wrong while processing jobs."

    return "\n\n".join(results) if results else "No jobs found 🫠"
