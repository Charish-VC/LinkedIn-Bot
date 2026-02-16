# tools/linkedin_scraper.py

import time
import random
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ⚠️ Chrome profile must NOT be open elsewhere
CHROME_PROFILE_PATH = r"C:\Users\chari\AppData\Local\Google\Chrome\User Data\SeleniumProfile"


def login_to_linkedin(browser):
    print("🌐 Opening LinkedIn...")
    browser.get("https://www.linkedin.com/")
    time.sleep(5)

    if "login" in browser.current_url:
        print("🔐 Please log in manually.")
        input("Press Enter after logging in...")

    return "linkedin.com" in browser.current_url


def scrape_jobs(keyword, location, max_jobs=25):
    print(f"🔍 Searching '{keyword}' in '{location}'")

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={CHROME_PROFILE_PATH}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    browser = webdriver.Chrome(options=options)
    wait = WebDriverWait(browser, 30)

    if not login_to_linkedin(browser):
        print("❌ Login failed")
        browser.quit()
        return []

    search_url = (
        "https://www.linkedin.com/jobs/search/"
        f"?keywords={quote(keyword)}&location={quote(location)}"
    )
    browser.get(search_url)
    time.sleep(3)

    # Wait for job cards
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.job-card-container"))
    )

    job_cards = browser.find_elements(By.CSS_SELECTOR, "div.job-card-container")
    print(f"🔍 Found {len(job_cards)} job cards")

    jobs = []
    seen_links = set()

    for card in job_cards[:max_jobs]:
        try:
            link_el = card.find_element(By.XPATH, ".//a[contains(@href,'/jobs/view')]")
            title = link_el.text.strip().split("\n")[0]
            link = link_el.get_attribute("href")

            if link in seen_links:
                continue
            seen_links.add(link)

            # Click job card to load description
            browser.execute_script("arguments[0].scrollIntoView(true);", card)
            card.click()
            time.sleep(random.uniform(2.0, 3.0))

            # Job description
            try:
                desc_el = wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div.jobs-description-content__text")
                    )
                )
                description = desc_el.text.strip()
            except Exception:
                description = ""

            # Company name
            try:
                company_el = card.find_element(By.CSS_SELECTOR, "h4 > a")
                company = company_el.text.strip()
            except Exception:
                company = ""

            jobs.append({
                "job_title": title,
                "company": company,
                "job_link": link,
                "job_description": description
            })

        except Exception as e:
            print(f"⚠️ Skipped job: {e}")

    browser.quit()
    print(f"✅ Extracted {len(jobs)} jobs")
    return jobs


# Standalone test
if __name__ == "__main__":
    jobs = scrape_jobs("Data Analyst", "Dubai")
    print(f"\n📊 Total jobs collected: {len(jobs)}")
    for i, job in enumerate(jobs[:5], 1):
        print(f"{i}. {job['job_title']} | {job['company']}")
