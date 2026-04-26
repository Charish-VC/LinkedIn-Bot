# tools/linkedin_scraper.py

import os
import time
import random
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def login_to_linkedin(browser):
    print("🌐 Opening LinkedIn...")
    browser.get("https://www.linkedin.com/")
    time.sleep(5)

    if "login" in browser.current_url:
        print("🔐 Please log in manually.")
        input("Press Enter after logging in...")

    return "linkedin.com" in browser.current_url


def get_driver_options(config):
    options = Options()
    
    chrome_path = config.get("selenium", {}).get("chrome_profile_path")
    if chrome_path:
        options.add_argument(f"--user-data-dir={chrome_path}")
    
    options.add_argument("--profile-directory=Default")
    options.add_argument("--start-maximized")
    
    if config.get("scraping", {}).get("anti_detection", True):
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
    
    return options


def human_delay(config):
    scraping_config = config.get("scraping", {})
    min_delay = scraping_config.get("min_delay_seconds", 2.0)
    max_delay = scraping_config.get("max_delay_seconds", 4.0)
    time.sleep(random.uniform(min_delay, max_delay))


def scrape_jobs(keyword, location, max_jobs=25, config=None):
    if config is None:
        config = {"scraping": {}, "selenium": {}}
    
    print(f"🔍 Searching '{keyword}' in '{location}'")

    options = get_driver_options(config)
    browser = webdriver.Chrome(options=options)
    
    if config.get("scraping", {}).get("anti_detection", True):
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            """
        })
    
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
    
    page_wait = config.get("scraping", {}).get("page_load_wait_seconds", 3)
    time.sleep(page_wait)

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

            browser.execute_script("arguments[0].scrollIntoView(true);", card)
            card.click()
            human_delay(config)

            try:
                desc_el = wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div.jobs-description-content__text")
                    )
                )
                description = desc_el.text.strip()
            except Exception:
                description = ""

            try:
                company_el = card.find_element(By.CSS_SELECTOR, "h4 > a")
                company = company_el.text.strip()
            except Exception:
                company = ""

            jobs.append({
                "job_title": title,
                "company": company,
                "job_link": link,
                "job_description": description,
                "date_applied": time.strftime("%Y-%m-%d"),
                "status": "pending"
            })

        except Exception as e:
            print(f"⚠️ Skipped job: {e}")

    browser.quit()
    print(f"✅ Extracted {len(jobs)} jobs")
    return jobs


if __name__ == "__main__":
    import yaml
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    jobs = scrape_jobs("Data Analyst", "Dubai", config=config)
    print(f"\n📊 Total jobs collected: {len(jobs)}")
    for i, job in enumerate(jobs[:5], 1):
        print(f"{i}. {job['job_title']} | {job['company']}")