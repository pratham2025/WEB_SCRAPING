# worker_linux.py — Linux-compatible worker for GitHub Actions (single cycle)

import time
import logging
import json
import importlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(filename)s] - %(message)s')
MAX_ANNOUNCEMENTS_PER_SOURCE = 60

# --- Load Supabase Credentials ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    logging.error("❌ Missing SUPABASE_URL or SUPABASE_KEY in environment. Exiting.")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Selenium Setup for Linux ---
def setup_driver():
    """Initializes Chrome driver for Linux (GitHub Actions compatible)."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=3")
    # Additional stability options for GitHub Actions
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-features=TranslateUI")
    options.add_argument("--disable-ipc-flooding-protection")
    
    # Use undetected_chromedriver for Linux (auto-detects ChromeDriver)
    try:
        driver = uc.Chrome(options=options, version_main=None)
        
        # Set explicit timeouts to handle slow connections and page loads
        # Page load timeout: 180 seconds (3 minutes) - increased for slow pages
        driver.set_page_load_timeout(180)
        # Script timeout: 60 seconds - for JavaScript execution
        driver.set_script_timeout(60)
        # Implicit wait: 10 seconds - for element finding
        driver.implicitly_wait(10)
        
        logging.info("Chrome driver initialized with extended timeouts (page_load: 180s, script: 60s, implicit: 10s)")
        return driver
    except Exception as e:
        logging.error(f"Failed to initialize Chrome driver: {e}")
        raise

# --- SAVE TO SUPABASE ---
def save_to_db(source_name, results):
    """Saves announcements directly to Supabase and notifies subscribers."""
    if not results:
        logging.info(f"No results to process for {source_name}.")
        return 0

    new_items_count = 0
    new_announcements = []
    try:
        for item in results:
            text = item.get("text")
            link = item.get("link")
            if not text:
                continue

            # Check for duplicates (same source & text)
            existing = supabase.table("announcements").select("id").eq("source", source_name).eq("text", text).execute()

            if not existing.data:
                payload = {
                    "source": source_name,
                    "text": text,
                    "link": link,
                    "scraped_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                }
                supabase.table("announcements").insert(payload).execute()
                new_items_count += 1
                # Track new announcements for email notifications
                new_announcements.append(payload)

        logging.info(f"✅ Supabase DB for {source_name}: Processed {len(results)} items, added {new_items_count} new.")
        
        # Notify subscribers if there are new announcements
        if new_announcements:
            try:
                from notify_subscribers import notify_subscribers
                emails_sent = notify_subscribers(source_name, new_announcements)
                if emails_sent > 0:
                    logging.info(f"📧 Sent email notifications to {emails_sent} subscribers for {source_name}")
            except Exception as e:
                logging.error(f"❌ Failed to notify subscribers for {source_name}: {e}")
                # Don't fail the entire scrape if email notification fails
        
        return new_items_count

    except Exception as e:
        logging.error(f"❌ Supabase error for {source_name}: {e}")
        return 0

# --- TASK FOR PARALLEL EXECUTION ---
def run_scraper_task(source_config, max_retries=2):
    """Manages the scraping process for a single source with retry logic."""
    source_name = source_config['name']
    url = source_config['url']
    logging.info(f"Starting task for: '{source_name}'")

    driver = None
    last_error = None
    
    try:
        for attempt in range(max_retries + 1):
            try:
                driver = setup_driver()
                module_name = f"scrapers.{source_name.lower()}_scraper"
                scraper_module = importlib.import_module(module_name)

                if source_name not in ["CBSE", "JEE"]:
                    logging.info(f"Loading URL for {source_name}: {url}")
                    driver.get(url)
                    # Give page a moment to stabilize after load
                    time.sleep(2)

                scraped_data = scraper_module.scrape(driver)

                # Limit announcements
                if scraped_data and len(scraped_data) > MAX_ANNOUNCEMENTS_PER_SOURCE:
                    logging.info(f"Source '{source_name}' has {len(scraped_data)} items. Limiting to {MAX_ANNOUNCEMENTS_PER_SOURCE}.")
                    scraped_data = scraped_data[:MAX_ANNOUNCEMENTS_PER_SOURCE]

                # Success - return result
                result = {"source": source_name, "data": scraped_data, "status": "Success"}
                return result

            except Exception as e:
                last_error = e
                error_msg = str(e)
                logging.warning(f"Task for '{source_name}' failed (attempt {attempt + 1}/{max_retries + 1}): {error_msg}")
                
                # Clean up driver on error
                if driver:
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    driver = None
                
                # If not the last attempt, wait before retrying
                if attempt < max_retries:
                    wait_time = (attempt + 1) * 5  # Exponential backoff: 5s, 10s
                    logging.info(f"Retrying {source_name} in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logging.error(f"Task for '{source_name}' failed after {max_retries + 1} attempts: {error_msg}", exc_info=True)

        # All retries exhausted
        return {"source": source_name, "data": [], "status": f"Failed: {last_error}"}
    
    finally:
        # Always clean up driver if it still exists
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
        logging.info(f"Finished task for: '{source_name}'")

# --- MAIN WORKER (SINGLE CYCLE) ---
def main():
    """Main worker function to run scrapers sequentially (single cycle for GitHub Actions)."""
    logging.info("🚀 Worker process starting (Linux/GitHub Actions mode - single cycle, sequential execution)")
    
    try:
        with open('config.json', 'r') as f:
            sources_to_scrape = json.load(f).get("sources", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"FATAL: Could not load or parse config.json: {e}. Exiting.")
        return

    cycle_start_time = time.time()
    logging.info("--- Starting SEQUENTIAL scraping cycle ---")

    total_new_items = 0
    successful_scrapes = 0
    failed_scrapes = 0

    # Run scrapers one at a time (sequential)
    for idx, source_config in enumerate(sources_to_scrape, 1):
        source_name = source_config['name']
        logging.info(f"[{idx}/{len(sources_to_scrape)}] Processing source: {source_name}")
        
        result = run_scraper_task(source_config)
        
        if result["status"] == "Success":
            new_items = save_to_db(result["source"], result["data"])
            total_new_items += new_items
            successful_scrapes += 1
            logging.info(f"✅ {source_name}: Scraped successfully, added {new_items} new items")
        else:
            failed_scrapes += 1
            logging.error(f"❌ {source_name}: Scraping failed - {result['status']}")

    cycle_end_time = time.time()

    logging.info("--- Scraping Cycle Summary ---")
    logging.info(f"Total time taken: {cycle_end_time - cycle_start_time:.2f} seconds")
    logging.info(f"Sources processed: {len(sources_to_scrape)}")
    logging.info(f"  - Successful: {successful_scrapes}")
    logging.info(f"  - Failed: {failed_scrapes}")
    logging.info(f"Total new announcements added to Supabase: {total_new_items}")
    logging.info("✅ Worker cycle completed successfully. Exiting (GitHub Actions will trigger next run).")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received. Shutting down worker.")
    except Exception as e:
        logging.error(f"❌ Fatal error in worker: {e}", exc_info=True)
        exit(1)

