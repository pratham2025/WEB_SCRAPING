import logging
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import time
import re

def scrape(driver):
    """
    Scrapes the RRB Ahmedabad 'News Updates' page using Selenium to handle dynamic content.
    Extracts: text, link, and article_date from each announcement block.
    """
    logging.info("Scraping RRB Ahmedabad website using Selenium-based method.")
    # The URL is loaded by worker.py, so we don't need to call driver.get() here.
    results = []

    try:
        # Increased wait time to 60 seconds for slow page loads and connection issues
        wait = WebDriverWait(driver, 60)
        # Wait for the first announcement block to be visible on the page
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.news-update-block")))
        time.sleep(2) # Pause to ensure all elements render

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all the div blocks that contain an individual announcement
        announcement_blocks = soup.find_all('div', class_='news-update-block shadow-block')

        if not announcement_blocks:
            logging.warning("RRB Ahmedabad: No announcement blocks were found even with Selenium.")
            return []

        for block in announcement_blocks:
            # Find the news-update-content div
            content_div = block.find('div', class_='news-update-content')
            if not content_div:
                continue

            # Find the link with class 'para-link' - this contains the announcement text and link
            link_tag = content_div.find('a', class_='para-link')
            
            if not link_tag or not link_tag.has_attr('href'):
                continue

            # Extract text - get all text but exclude the "NEW" badge image
            # Clone the tag to avoid modifying the original, then remove images
            link_clone = BeautifulSoup(str(link_tag), 'html.parser').find('a')
            if link_clone:
                # Remove any img tags (like the NEW badge)
                for img in link_clone.find_all('img'):
                    img.decompose()
                text = link_clone.get_text(separator=' ', strip=True)
            else:
                # Fallback: get text directly, but this might include image alt text
                text = link_tag.get_text(separator=' ', strip=True)

            # Extract the link
            link = urljoin(driver.current_url, link_tag['href'])

            # Extract the date - look for date patterns in the block
            # Date format appears to be DD/MM/YYYY (e.g., "08/12/2025")
            date = ""
            date_pattern = r'\d{2}/\d{2}/\d{4}'
            
            # First, try to find date in common date container elements
            # Look for elements that might contain dates (often after the link)
            date_candidates = block.find_all(['span', 'div', 'p', 'time'], class_=re.compile(r'date|time|published', re.I))
            for candidate in date_candidates:
                candidate_text = candidate.get_text(strip=True)
                date_match = re.search(date_pattern, candidate_text)
                if date_match:
                    date = date_match.group(0)
                    break
            
            # If not found in specific elements, search the entire block text
            if not date:
                block_text = block.get_text()
                date_match = re.search(date_pattern, block_text)
                if date_match:
                    date = date_match.group(0)

            # Only add if we have text and link
            if text and link:
                result_item = {
                    "text": text,
                    "link": link
                }
                # Add article_date if found
                if date:
                    result_item["article_date"] = date
                
                results.append(result_item)

        logging.info(f"Found {len(results)} announcements for RRB Ahmedabad.")

    except Exception as e:
        logging.error(f"An error occurred while scraping RRB Ahmedabad: {e}", exc_info=True)
        driver.save_screenshot('rrbahmedabad_error.png')

    return results