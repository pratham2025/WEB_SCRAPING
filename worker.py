# worker.py (Supabase Version — identical logic to your original local DB version)

import time
import logging
import json
import importlib
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import undetected_chromedriver as uc
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(filename)s] - %(message)s')
SCRAPE_INTERVAL_SECONDS = 3600
MAX_ANNOUNCEMENTS_PER_SOURCE = 60

# --- Load Supabase Credentials ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    logging.error("❌ Missing SUPABASE_URL or SUPABASE_KEY in .env file. Exiting.")
    exit()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Selenium Setup ---
def setup_driver():
    """Initializes Chrome driver using local fixed path to avoid re-download errors."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # ✅ Use your local ChromeDriver path
    service = ChromeService(r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=options)
    return driver

# --- SAVE TO SUPABASE ---
def save_to_db(source_name, results):
    """Saves announcements directly to Supabase."""
    if not results:
        logging.info(f"No results to process for {source_name}.")
        return 0

    new_items_count = 0
    try:
        for item in results:
            text = item.get("text")
            link = item.get("link")
            if not text:
                continue

            # Check for duplicates (same source & text)
            existing = supabase.table("announcements").select("id").eq("source", source_name).eq("text", text).execute()

            if not existing.data:
                supabase.table("announcements").insert({
                    "source": source_name,
                    "text": text,
                    "link": link,
                    "scraped_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                }).execute()
                new_items_count += 1

        logging.info(f"✅ Supabase DB for {source_name}: Processed {len(results)} items, added {new_items_count} new.")
        return new_items_count

    except Exception as e:
        logging.error(f"❌ Supabase error for {source_name}: {e}")
        return 0

# --- TASK FOR PARALLEL EXECUTION ---
def run_scraper_task(source_config):
    """Manages the scraping process for a single source."""
    source_name = source_config['name']
    url = source_config['url']
    logging.info(f"Starting task for: '{source_name}'")

    driver = None
    try:
        driver = setup_driver()
        module_name = f"scrapers.{source_name.lower()}_scraper"
        scraper_module = importlib.import_module(module_name)

        if source_name not in ["CBSE", "JEE"]:
            driver.get(url)

        scraped_data = scraper_module.scrape(driver)

        # Limit announcements
        if scraped_data and len(scraped_data) > MAX_ANNOUNCEMENTS_PER_SOURCE:
            logging.info(f"Source '{source_name}' has {len(scraped_data)} items. Limiting to {MAX_ANNOUNCEMENTS_PER_SOURCE}.")
            scraped_data = scraped_data[:MAX_ANNOUNCEMENTS_PER_SOURCE]

        return {"source": source_name, "data": scraped_data, "status": "Success"}

    except Exception as e:
        logging.error(f"Task for '{source_name}' failed: {e}", exc_info=False)
        return {"source": source_name, "data": [], "status": f"Failed: {e}"}

    finally:
        if driver:
            driver.quit()
        logging.info(f"Finished task for: '{source_name}'")

# --- MAIN WORKER LOOP ---
def main():
    """Main worker loop to run scrapers in parallel."""
    logging.info("Worker process starting.")
    try:
        with open('config.json', 'r') as f:
            sources_to_scrape = json.load(f).get("sources", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"FATAL: Could not load or parse config.json: {e}. Exiting.")
        return

    while True:
        cycle_start_time = time.time()
        logging.info("--- Starting new PARALLEL scraping cycle ---")

        results_summary = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_source = {executor.submit(run_scraper_task, config): config for config in sources_to_scrape}

            for future in concurrent.futures.as_completed(future_to_source):
                result = future.result()
                results_summary.append(result)

        total_new_items = 0
        successful_scrapes = 0
        failed_scrapes = 0

        for result in results_summary:
            if result["status"] == "Success":
                new_items = save_to_db(result["source"], result["data"])
                total_new_items += new_items
                successful_scrapes += 1
            else:
                failed_scrapes += 1
                logging.error(f"Skipping database save for {result['source']} due to scraping failure.")

        cycle_end_time = time.time()

        logging.info("--- Scraping Cycle Summary ---")
        logging.info(f"Total time taken: {cycle_end_time - cycle_start_time:.2f} seconds")
        logging.info(f"Sources processed: {len(sources_to_scrape)}")
        logging.info(f"  - Successful: {successful_scrapes}")
        logging.info(f"  - Failed: {failed_scrapes}")
        logging.info(f"Total new announcements added to Supabase: {total_new_items}")
        logging.info(f"--- Waiting for {SCRAPE_INTERVAL_SECONDS} seconds for next cycle ---")

        time.sleep(SCRAPE_INTERVAL_SECONDS)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received. Shutting down worker.")
