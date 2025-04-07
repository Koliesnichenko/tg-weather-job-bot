import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_djinni_jobs_selenium():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    CHROMEDRIVER_PATH = os.path.join(os.getcwd(), "chromedriver.exe")
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://djinni.co/jobs/?keywords=python&primary_keyword=Python")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.mb-4[id^='job-item']"))
        )
    except:
        driver.quit()
        return "❗ Timeout: Djinni didn't load job listings."

    jobs = []
    job_cards = driver.find_elements(By.CSS_SELECTOR, "li.mb-4[id^='job-item']")
    print(f"Found {len(job_cards)} jobs")

    for job in job_cards[:5]:
        try:
            title_elem = job.find_element(By.CLASS_NAME, "job-item__title-link")
            title = title_elem.text.strip()
            href = title_elem.get_attribute("href")
            link = href if href.startswith("http") else "https://djinni.co" + href

            try:
                company_elem = job.find_element(By.CLASS_NAME, "job-item__company")
                company = company_elem.text.strip()
            except:
                company = "Unknown company"

            jobs.append(f"💼 {title}\n🏢 {company}\n🔗 {link}")
        except Exception as e:
            print("⚠️ Error in job block:", e)
            continue

    driver.quit()
    return "\n\n".join(jobs) if jobs else "❗ Djinni returned no jobs or layout changed."
