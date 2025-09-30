# worker.py (Updated with a 60-item limit per source)

import psycopg2
import time
import logging
import json
import importlib
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

# --- NEW: Import the summary generation function ---
from summarizer import generate_summary

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(module)s] - %(message)s')
SCRAPE_INTERVAL_SECONDS = 3600
# --- NEW: Set a limit for announcements per source ---
MAX_ANNOUNCEMENTS_PER_SOURCE = 60

# --- Selenium Setup (No changes needed here) ---
def setup_driver():
    """Initializes an UNDETECTED headless Chrome WebDriver."""
    options = uc.ChromeOptions()
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
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

# --- DATABASE OPERATIONS (No changes needed here) ---
def save_to_db(source_name, results_with_summaries):
    """Saves results with their summaries to the database."""
    if not results_with_summaries:
        logging.info(f"No results to process for {source_name}.")
        return 0

    # The results are already unique from the scraper task
    conn_params = {
        "host": "localhost", "dbname": "announcements_db", "user": "notifyme",
        "password": "Pratham@2025", "port": "5432"
    }
    new_items_count = 0
    conn = None
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        sql_insert_query = """
            INSERT INTO announcements (source, text, link, summary) 
            VALUES (%s, %s, %s, %s) 
            ON CONFLICT (source, text) DO NOTHING
        """
        
        for item in results_with_summaries:
            cursor.execute(sql_insert_query, (source_name, item['text'], item['link'], item['summary']))
            if cursor.rowcount > 0:
                new_items_count += 1
        conn.commit()
    except psycopg2.Error as e:
        logging.error(f"Database error for {source_name}: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()
    
    logging.info(f"Database for {source_name} complete. Processed {len(results_with_summaries)} items, added {new_items_count} new.")
    return new_items_count

# --- TASK FOR PARALLEL EXECUTION (MODIFIED) ---
def run_scraper_task(source_config):
    """
    Manages scraping AND summarization for a single source within a thread.
    """
    source_name = source_config['name']
    url = source_config['url']
    logging.info(f"Starting task for: '{source_name}'")
    
    driver = None  # Initialize driver to None
    try:
        driver = setup_driver()
        module_name = f"scrapers.{source_name.lower()}_scraper"
        scraper_module = importlib.import_module(module_name)
        
        if source_name not in ["CBSE", "JEE"]:
            driver.get(url)
        
        scraped_data = scraper_module.scrape(driver)

        # --- MODIFIED: Limit the number of announcements before processing ---
        if scraped_data and len(scraped_data) > MAX_ANNOUNCEMENTS_PER_SOURCE:
            logging.info(f"Source '{source_name}' has {len(scraped_data)} items. Limiting to the first {MAX_ANNOUNCEMENTS_PER_SOURCE}.")
            # Slice the list to get only the first 60 items
            scraped_data = scraped_data[:MAX_ANNOUNCEMENTS_PER_SOURCE]
        
        # --- Process data and generate summaries right after scraping ---
        processed_data = []
        if scraped_data:
            logging.info(f"Found {len(scraped_data)} items for '{source_name}'. Generating summaries...")
            for item in scraped_data:
                # Generate summary for the original text
                summary = generate_summary(item['text'])
                # Append the summary to the item dictionary
                item['summary'] = summary
                processed_data.append(item)
            logging.info(f"Summarization complete for '{source_name}'.")
        
        return {"source": source_name, "data": processed_data, "status": "Success"}
    except Exception as e:
        logging.error(f"Task for '{source_name}' failed: {e}", exc_info=False)
        return {"source": source_name, "data": [], "status": f"Failed: {e}"}
    finally:
        if driver:
            driver.quit()
        logging.info(f"Finished task for: '{source_name}'")

# --- MAIN WORKER ORCHESTRATOR (No changes needed here) ---
def main():
    """Main worker loop to run scrapers in parallel and provide a summary."""
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

        # --- Process all results after scraping is done ---
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
        
        # --- Final Summary Report ---
        logging.info("--- Scraping Cycle Summary ---")
        logging.info(f"Total time taken: {cycle_end_time - cycle_start_time:.2f} seconds")
        logging.info(f"Sources processed: {len(sources_to_scrape)}")
        logging.info(f"  - Successful: {successful_scrapes}")
        logging.info(f"  - Failed: {failed_scrapes}")
        logging.info(f"Total new announcements added to DB: {total_new_items}")
        logging.info(f"--- Waiting for {SCRAPE_INTERVAL_SECONDS} seconds for next cycle ---")
        
        time.sleep(SCRAPE_INTERVAL_SECONDS)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received. Shutting down worker.")