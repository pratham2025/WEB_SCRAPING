import psycopg2
import time
import logging
import json
import importlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

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

# --- DATABASE OPERATIONS ---
def save_to_db(source_name, results):
    if not results:
        logging.warning(f"No results to save for {source_name}.")
        return

    unique_results = []
    seen_texts = set()
    for item in results:
        if item['text'] not in seen_texts:
            unique_results.append(item)
            seen_texts.add(item['text'])

    # IMPORTANT: Use environment variables for these in production!
    conn_params = {
        "host": "localhost",
        "dbname": "announcements_db",
        "user": "notifyme",
        "password": "Pratham@2025",
        "port": "5432"
    }
    conn = None
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
        logging.info(f"Database for {source_name} complete. Added {new_items_count} new items.")
    except psycopg2.Error as e:
        logging.error(f"Database error for {source_name}: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()

# --- Main Worker Loop ---
def main():
    """Main worker loop to dynamically run scrapers."""
    logging.info("Worker process starting.")
    try:
        with open('config.json', 'r') as f:
            sources_to_scrape = json.load(f).get("sources", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"FATAL: Could not load or parse config.json: {e}. Exiting.")
        return

    driver = setup_driver()
    try:
        while True:
            logging.info("--- Starting new scraping cycle ---")
            for source_config in sources_to_scrape:
                source_name = source_config['name']
                url = source_config['url']
                
                try:
                    # Dynamically import the scraper module from the 'scrapers' folder
                    # e.g., for "MPSC", it will look for "scrapers.mpsc_scraper"
                    module_name = f"scrapers.{source_name.lower()}_scraper"
                    scraper_module = importlib.import_module(module_name)
                    
                    logging.info(f"Processing source: '{source_name}'")
                    
                    # For scrapers using requests-first, driver is passed but may not be used initially
                    if source_name not in ["CBSE", "JEE"]:
                         driver.get(url)

                    # Call the 'scrape' function from the imported module
                    scraped_data = scraper_module.scrape(driver)
                    
                    save_to_db(source_name, scraped_data)
                except ImportError:
                    logging.warning(f"No scraper found for '{source_name}' at {module_name}.py. Skipping.")
                except Exception as e:
                    logging.error(f"An unhandled error occurred for '{source_name}': {e}", exc_info=True)

            logging.info(f"--- Scraping cycle complete. Waiting for {SCRAPE_INTERVAL_SECONDS} seconds. ---")
            time.sleep(SCRAPE_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received. Shutting down worker.")
    finally:
        driver.quit()
        logging.info("WebDriver closed. Worker process finished.")

if __name__ == '__main__':
    main()