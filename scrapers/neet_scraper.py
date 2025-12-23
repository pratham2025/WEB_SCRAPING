import logging
import time
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def scrape_neet_selenium(driver):
    """Scrapes NEET website using Selenium."""
    logging.info("NEET: Attempting to scrape using Selenium.")
    try:
        # Increased wait time to 60 seconds for slow page loads and connection issues
        wait = WebDriverWait(driver, 60)
        # Wait for the gen-list div to be present (as shown in screenshot)
        # Try multiple selectors to ensure we find the elements
        selectors = [
            ".wpb_wrapper .gen-list ul li a",
            ".wpb_wrapper .gen-list.default-list ul li a",
            ".wpb_wrapper ul li a"
        ]
        
        element_found = False
        for selector in selectors:
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                element_found = True
                logging.info(f"Found elements using selector: {selector}")
                break
            except TimeoutException:
                continue
        
        if not element_found:
            logging.error("Could not find any announcement elements on the page")
            return []
        
        time.sleep(2)  # Give page time to fully render
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = []
        
        # Try multiple selectors to find announcements
        for selector in selectors:
            items = soup.select(selector)
            if items:
                logging.info(f"Found {len(items)} items using selector: {selector}")
                for item in items:
                    text = item.get_text(strip=True)
                    link = item.get("href", "#")
                    if text:
                        if not link.startswith("http"):
                            link = urljoin(driver.current_url, link)
                        results.append({"text": text, "link": link})
                break
        
        # Remove duplicates while preserving order
        seen = set()
        unique_results = []
        for result in results:
            result_key = (result["text"], result["link"])
            if result_key not in seen:
                seen.add(result_key)
                unique_results.append(result)
        
        logging.info(f"Found {len(unique_results)} unique announcements for NEET (selenium).")
        return unique_results
    except TimeoutException as e:
        logging.error(f"Timeout waiting for NEET page elements: {e}")
        return []
    except Exception as e:
        logging.error(f"Error during Selenium scraping for NEET: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return []

def scrape(driver):
    """Scrapes the NEET website using a requests-first approach (like JEE)."""
    logging.info("NEET: Attempting to scrape using requests method.")
    url = "https://neet.nta.nic.in/public-notices/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # Try requests first (faster, more reliable)
        res = requests.get(url, headers=headers, timeout=20)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        results = []
        
        # Try multiple selectors based on screenshot structure
        # Structure: .wpb_wrapper > .gen-list.default-list > ul > li > a
        selectors = [
            ".wpb_wrapper .gen-list ul li a",
            ".wpb_wrapper .gen-list.default-list ul li a",
            ".wpb_wrapper ul li a"
        ]
        
        for selector in selectors:
            items = soup.select(selector)
            if items:
                logging.info(f"Found {len(items)} items using selector: {selector}")
                for item in items:
                    text = item.get_text(strip=True)
                    link = item.get("href", "#")
                    if text:
                        if not link.startswith("http"):
                            link = urljoin(url, link)
                        results.append({"text": text, "link": link})
                break
        
        # Remove duplicates while preserving order
        seen = set()
        unique_results = []
        for result in results:
            result_key = (result["text"], result["link"])
            if result_key not in seen:
                seen.add(result_key)
                unique_results.append(result)
        
        if unique_results:
            logging.info(f"Found {len(unique_results)} unique announcements for NEET (requests).")
            return unique_results
        else:
            logging.warning("No results found with requests method, falling back to Selenium.")
            return scrape_neet_selenium(driver)
            
    except Exception as e:
        logging.error(f"Requests failed for NEET: {e}")
        return scrape_neet_selenium(driver)