import os
import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_djinni_jobs_selenium(query="python", limit=5):
    """
    Universal Djinni scraper with custom keyword and result limit.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
    jobs = []

    try:
        service = Service(executable_path=CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)

        url = f"https://djinni.co/jobs/?keywords={query}&primary_keyword={query}"
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.mb-4[id^='job-item']"))
            )
        except Exception:
            return f"❗ Timeout: Djinni didn't load job listings for '{query}'."

        job_cards = driver.find_elements(By.CSS_SELECTOR, "li.mb-4[id^='job-item']")
        logging.info(f"🔍 Found {len(job_cards)} jobs on Djinni for query: '{query}'")

        for job in job_cards[:limit]:
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
                logging.warning(f"⚠️ Error in job block: {e}")
                continue

    except Exception as e:
        logging.error(f"🚨 Selenium error: {e}")
        return f"❗ Failed to scrape Djinni for query: '{query}'"

    finally:
        try:
            driver.quit()
        except Exception:
            pass

    return "\n\n".join(jobs) if jobs else f"❗ Djinni returned no jobs for '{query}'"
