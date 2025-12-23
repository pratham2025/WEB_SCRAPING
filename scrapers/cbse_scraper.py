import logging
import time
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_cbse_selenium(driver):
    logging.warning("CBSE: Requests method failed, falling back to Selenium.")
    try:
        # Increased wait time to 60 seconds for slow page loads and connection issues
        wait = WebDriverWait(driver, 60)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.list-new a")))
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = []
        for item in soup.select("li.list-new a"):
            text = item.text.strip()
            link = urljoin(driver.current_url, item.get("href", "#"))
            results.append({"text": text, "link": link})
        return results
    except Exception as e:
        logging.error(f"Error during Selenium fallback for CBSE: {e}")
        return []

def scrape(driver):
    """Scrapes the CBSE website using a requests-first approach."""
    logging.info("CBSE: Attempting to scrape using requests method.")
    url = "https://www.cbse.gov.in/cbsenew/cbse.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=20)
        res.raise_for_status()
        if "Access Denied" in res.text:
            logging.error("CBSE blocked requests method.")
            return scrape_cbse_selenium(driver)
        soup = BeautifulSoup(res.text, "html.parser")
        results = []
        for item in soup.select("li.list-new a"):
            text = item.text.strip()
            link = urljoin(url, item.get("href", "#"))
            results.append({"text": text, "link": link})
        logging.info(f"Found {len(results)} announcements for CBSE.")
        return results
    except requests.RequestException as e:
        logging.error(f"Requests failed for CBSE: {e}")
        return scrape_cbse_selenium(driver)