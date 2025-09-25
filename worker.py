import psycopg2
import os
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
from selenium.webdriver.common.keys import Keys
# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(filename)s] - %(message)s')
SCRAPE_INTERVAL_SECONDS = 3600

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
# (All scraper functions remain unchanged)
def scrape_mahacet(driver):
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

def scrape_cbse_selenium(driver):
    logging.warning("CBSE: Requests method failed, falling back to Selenium.")
    try:
        wait = WebDriverWait(driver, 15)
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

def scrape_cbse(driver):
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
        return results
    except requests.RequestException as e:
        logging.error(f"Requests failed for CBSE: {e}")
        return scrape_cbse_selenium(driver)

def scrape_neet(driver):
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

def scrape_jee_selenium(driver):
    logging.warning("JEE: Requests method failed, falling back to Selenium.")
    try:
        wait = WebDriverWait(driver, 25)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".wpb_wrapper .gen-list ul li a")))
        time.sleep(2)
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
        logging.error(f"Error during Selenium fallback for JEE: {e}")
        return []

def scrape_jee(driver):
    logging.info("JEE: Attempting to scrape using requests method.")
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
        return scrape_jee_selenium(driver)

def scrape_gate(driver):
    """Scrapes announcements from the GATE 2026 website, creating unique placeholders for items without links."""
    logging.info("Scraping GATE 2026 website.")
    results = []
    try:
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-bordered")))
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        notification_table = soup.find('table', class_='table-bordered')
        if not notification_table:
            logging.warning("GATE: Could not find the notification table.")
            return []
        for row in notification_table.find_all('tr'):
            cell = row.find('td', class_='text-left')
            if not cell:
                continue
            
            text = cell.get_text(strip=True)
            link_tag = cell.find('a')

            if link_tag and link_tag.get('href', '#') != '#':
                link = link_tag.get('href')
            else:
                placeholder = text.replace(' ', '-').replace('.', '')
                link = f"#{placeholder}"

            if text:
                if not link.startswith('http') and not link.startswith('#'):
                    link = urljoin(driver.current_url, link)
                results.append({"text": text, "link": link})

    except TimeoutException:
        logging.error("GATE: Timed out waiting for the notifications table to load.")
    except Exception as e:
        logging.error(f"An unexpected error occurred while scraping GATE: {e}")
        
    logging.info(f"Found {len(results)} announcements for GATE.")
    return results


def scrape_upsc(driver):
    """Scrapes all announcements from UPSC, including those without links."""
    logging.info("Scraping UPSC website.")
    results = []
    try:
        wait = WebDriverWait(driver, 20)
        target_div_selector = (By.CSS_SELECTOR, "div.scroll-content")
        wait.until(EC.presence_of_element_located(target_div_selector))
        time.sleep(3) # Extra wait for all JS to render

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        announcement_div = soup.find('div', class_='scroll-content')
        if not announcement_div:
            logging.warning("UPSC: Could not find the announcement container.")
            return []

        # Find all span tags, which act as containers for each announcement
        for item_span in announcement_div.find_all('span'):
            # Get the full text from the span, skipping any empty/styling spans
            full_text = item_span.get_text(strip=True)
            if not full_text:
                continue

            link_tag = item_span.find('a')
            
            if link_tag:
                # If a link tag exists, use its text and href
                text = link_tag.get_text(strip=True)
                link = link_tag.get('href', '#')
            else:
                # If NO link tag, use the span's full text and create a placeholder
                text = full_text
                # This makes the item unique so it can be saved to the database
                placeholder = text.replace(' ', '-').replace('.', '').replace('(', '').replace(')', '')
                link = f"#{placeholder}"
            
            # Make the link absolute if it's a real URL
            if not link.startswith('http') and not link.startswith('#'):
                link = urljoin(driver.current_url, link)
            
            results.append({"text": text, "link": link})
    
    except TimeoutException:
        logging.error("UPSC: Timed out waiting for the announcements to load.")
    except Exception as e:
        logging.error(f"An unexpected error occurred while scraping UPSC: {e}")
        
    logging.info(f"Found {len(results)} announcements for UPSC.")
    return results

# worker.py (new scrape_mpsc function)

def scrape_mpsc(driver):
    """Scrapes the MPSC advertisements page using Selenium (ensures unique text)."""
    logging.info("Scraping MPSC advertisements page using Selenium.")
    results = []
    base_url = "https://mpsc.gov.in"

    try:
        # Wait for table to load
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.ID, "datatable")))
        time.sleep(2)

        # Get all rows from Selenium
        rows = driver.find_elements(By.CSS_SELECTOR, "#datatable tbody tr")

        seen_texts = set()  # Keep track of unique text

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 5:
                continue

            adv_no = cols[1].text.strip()       # 2nd column
            subject_text = cols[2].text.strip() # 3rd column
            pub_date = cols[3].text.strip()     # 4th column

            # PDF link (5th column)
            try:
                pdf_tag = cols[4].find_element(By.TAG_NAME, "a")
                pdf_link = pdf_tag.get_attribute("href")
            except:
                pdf_link = None

            if not subject_text:
                continue

            # Create clean text for uniqueness
            clean_text = f"{adv_no} | {subject_text} | {pub_date}".replace('\n', ' ').strip()

            if clean_text in seen_texts:
                continue  # Skip duplicate text in same batch

            seen_texts.add(clean_text)

            # If link is missing, create a placeholder
            link = pdf_link if pdf_link else f"#{adv_no}-{pub_date}"

            results.append({
                "text": clean_text,
                "link": link
            })

    except TimeoutException:
        logging.error("MPSC: Timed out waiting for table.")
        driver.save_screenshot("mpsc_error_screenshot.png")
    except Exception as e:
        logging.error(f"MPSC: Unexpected error - {e}")

    logging.info(f"Found {len(results)} announcements for MPSC.")
    return results




# --- DATABASE OPERATIONS (Notification Style) ---
def save_to_db(source_name, results):
    if not results:
        logging.warning(f"No results to save for {source_name}.")
        return

    # Filter duplicates in the current batch by text
    unique_results = []
    seen_texts = set()
    for item in results:
        if item['text'] not in seen_texts:
            unique_results.append(item)
            seen_texts.add(item['text'])

    conn_params = {
        "host": "localhost",
        "dbname": "announcements_db",
        "user": "notifyme",
        "password": "Pratham@2025",
        "port": "5432"
    }

    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        new_items_count = 0

        for item in unique_results:
            cursor.execute(
                """
                INSERT INTO announcements (source, text, link) 
                VALUES (%s, %s, %s)
                ON CONFLICT (source, text) DO NOTHING
                """,
                (source_name, item['text'], item['link'])
            )
            if cursor.rowcount > 0:
                new_items_count += 1

        conn.commit()
        logging.info(f"Database operation for {source_name} complete. Added {new_items_count} new items.")

    except psycopg2.Error as e:
        logging.error(f"Database error for {source_name}: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# --- Main Worker Loop ---
def main():
    """Main worker loop to run scrapers at a set interval."""
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
        "GATE": scrape_gate,
        "UPSC": scrape_upsc,
        "MPSC": scrape_mpsc,
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
                    # Logic for scrapers that use Selenium to navigate
                    # CBSE & JEE use a 'requests-first' approach inside their functions
                    if source_name not in ["CBSE", "JEE"]:
                        driver.get(url)
                    
                    # Call the appropriate scraper function, passing the driver
                    scraped_data = scraper_function(driver)
                    
                    # Save the results to the database
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