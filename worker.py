import sqlite3
import time
import logging
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
import requests

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(filename)s] - %(message)s')
SCRAPE_INTERVAL_SECONDS = 3600  # Scrape every 1 hour

# --- Selenium Setup ---
def setup_driver():
    """Initializes a headless Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

# --- Site-Specific Scraper Functions ---

def scrape_mahacet(driver):
    """
    Scrapes announcements from the MAHACET website.
    Uses the user's original, proven logic.
    """
    logging.info("Using original, user-provided logic for MAHACET.")
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'educms-download-marquee-content-items')))
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = []
    announcement_list = soup.find('ul', class_='educms-download-marquee-content-items')
    if announcement_list:
        for item in announcement_list.find_all('li'):
            link_tag = item.find('a')
            if link_tag and link_tag.text.strip():
                text = link_tag.text.strip()
                link = link_tag.get('href', '#')
                if not link.startswith('http'):
                    link = urljoin(driver.current_url, link)
                results.append({"text": text, "link": link})
    logging.info(f"Found {len(results)} announcements for MAHACET.")
    return results

def scrape_nta(driver):
    """Scrapes announcements from the NTA website."""
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'latestPart')))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = []
    notice_box = soup.find('marquee', class_='latestPart')
    if notice_box:
        for item in notice_box.find_all('p'):
            text_tag = item.find('content')
            link_tag = item.find('a')
            if text_tag and link_tag and text_tag.text.strip():
                link = link_tag.get('href', '#')
                if not link.startswith('http'):
                    link = urljoin("https://www.nta.ac.in/", link)
                results.append({"text": text_tag.text.strip(), "link": link})
    return results


def scrape_cbse_requests():
    """Scrape CBSE using requests (fallback when Selenium is blocked)."""
    logging.info("CBSE: Using requests fallback method.")
    url = "https://www.cbse.gov.in/cbsenew/cbse.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=20)
        res.raise_for_status()
        if "Access Denied" in res.text:
            logging.error("CBSE blocked requests method as well.")
            return []
        soup = BeautifulSoup(res.text, "html.parser")
        results = []
        for item in soup.select("li.list-new a"):
            text = item.text.strip()
            link = urljoin(url, item.get("href", "#"))
            results.append({"text": text, "link": link})
        return results
    except requests.RequestException as e:
        logging.error(f"Requests failed for CBSE: {e}")
        return []

def scrape_cbse(driver):
    """Scrapes announcements from the CBSE website using Selenium, with a built-in fallback."""
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#box1")))
        time.sleep(4)

        if "Access Denied" in driver.page_source:
            logging.warning("CBSE blocked Selenium, falling back to requests.")
            return scrape_cbse_requests()

        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = []
        for item in soup.select("li.list-new a"):
            text = item.text.strip()
            link = urljoin(driver.current_url, item.get("href", "#"))
            results.append({"text": text, "link": link})
        return results
    except Exception as e:
        logging.error(f"Error during Selenium scrape for CBSE: {e}")
        return scrape_cbse_requests()

def scrape_neet(driver):
    """Scrapes public notices from the NEET website."""
    logging.info("Scraping NEET website.")
    wait = WebDriverWait(driver, 20)
    
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".wpb_wrapper ul li a")))
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = []
    
    notice_list = soup.select_one(".wpb_wrapper ul")
    if notice_list:
        for item in notice_list.find_all('li'):
            link_tag = item.find('a')
            if link_tag and link_tag.text.strip():
                text = link_tag.text.strip()
                link = link_tag.get('href', '#')
                if not link.startswith('http'):
                    link = urljoin(driver.current_url, link)
                results.append({"text": text, "link": link})
    
    logging.info(f"Found {len(results)} announcements for NEET.")
    return results

def scrape_jee_requests():
    """Scrape JEE Main using requests fallback."""
    logging.info("JEE: Using requests fallback method.")
    url = "https://jeemain.nta.nic.in/public-notices/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=20)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        results = []
        for item in soup.select(".wpb_wrapper .gen-list ul li a"):
            text = item.get_text(strip=True)
            link = item.get("href", "#")
            if text:
                if not link.startswith("http"):
                    link = urljoin(url, link)
                results.append({"text": text, "link": link})
        logging.info(f"Found {len(results)} announcements for JEE (requests).")
        return results
    except Exception as e:
        logging.error(f"Requests failed for JEE: {e}")
        return []


def scrape_jee(driver):
    """Scrapes public notices from the JEE Main website using Selenium, with fallback."""
    logging.info("Scraping JEE Main website.")
    try:
        wait = WebDriverWait(driver, 25)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".wpb_wrapper .gen-list ul li a")))
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = []
        for item in soup.select(".wpb_wrapper .gen-list ul li a"):
            text = item.get_text(strip=True)
            link = item.get("href", "#")
            if text:
                if not link.startswith("http"):
                    link = urljoin(driver.current_url, link)
                results.append({"text": text, "link": link})

        logging.info(f"Found {len(results)} announcements for JEE (selenium).")
        return results
    except Exception as e:
        logging.error(f"Error scraping JEE: {e}")
        return scrape_jee_requests()


# --- Database Operations ---
def save_to_db(source_name, results):
    if not results:
        logging.warning(f"No results to save for {source_name}.")
        return

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    new_items_count = 0
    for item in reversed(results):
        try:
            cursor.execute("INSERT OR IGNORE INTO announcements (source, text, link) VALUES (?, ?, ?)",
                           (source_name, item['text'], item['link']))
            if cursor.rowcount > 0:
                new_items_count += 1
        except Exception as e:
            logging.error(f"Database error for {source_name}: {e} - Item: {item}")
    conn.commit()
    conn.close()
    logging.info(f"Finished database operation for {source_name}. Added {new_items_count} new items.")

# --- Main Worker Loop ---
def main():
    logging.info("Worker process starting.")
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"FATAL: Could not load or parse config.json: {e}. Exiting.")
        return

    sources_to_scrape = config.get("sources", [])
    if not sources_to_scrape:
        logging.error("No sources found in config.json. Exiting.")
        return

    SCRAPERS = {
        "MAHACET": scrape_mahacet,
        "NTA": scrape_nta,
        "CBSE": scrape_cbse,
        "NEET": scrape_neet,
        "JEE": scrape_jee,
    }

    driver = setup_driver()
    
    try:
        while True:
            logging.info("--- Starting new scraping cycle ---")
            for source_config in sources_to_scrape:
                source_name = source_config['name']
                url = source_config['url']
                scraper_function = SCRAPERS.get(source_name)

                if not scraper_function:
                    logging.warning(f"No scraper function defined for '{source_name}'. Skipping.")
                    continue
                
                logging.info(f"Processing source: '{source_name}'")
                try:
                    driver.get(url)
                    scraped_data = scraper_function(driver)
                    save_to_db(source_name, scraped_data)
                except Exception as e:
                    logging.error(f"A critical, unhandled error occurred for '{source_name}': {e}")
            
            logging.info(f"--- Scraping cycle complete. Waiting for {SCRAPE_INTERVAL_SECONDS} seconds. ---")
            time.sleep(SCRAPE_INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received. Shutting down worker.")
    finally:
        driver.quit()
        logging.info("WebDriver closed. Worker process finished.")

if __name__ == '__main__':
    main()

