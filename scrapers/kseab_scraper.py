import logging
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import time

def scrape(driver):
    """
    Scrapes the KSEAB 'Latest News' marquee section by targeting the marquee tag.
    """
    logging.info("Scraping KSEAB website by targeting the marquee element.")
    results = []

    try:
        # Increased wait time from 20 to 60 seconds for slow page loads
        wait = WebDriverWait(driver, 60)
        # Wait for the unique container with id='newsTicker10' to be visible.
        wait.until(EC.visibility_of_element_located((By.ID, "newsTicker10")))
        time.sleep(2)  # Increased from 1 to 2 seconds for page stability

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the marquee element directly, as shown in your screenshot.
        news_marquee = soup.find('marquee', class_='marquee')
        if not news_marquee:
            logging.error("KSEAB: Could not find the marquee element.")
            driver.save_screenshot('kseab_error.png')
            return []

        # Find all the links within the marquee.
        announcement_links = news_marquee.find_all('a')

        if not announcement_links:
            logging.warning("KSEAB: No announcement links were found in the marquee.")
            return []

        for link_tag in announcement_links:
            if link_tag and link_tag.has_attr('href'):
                text = link_tag.get_text(strip=True)
                link = urljoin(driver.current_url, link_tag['href'])

                if text and link:
                    results.append({"text": text, "link": link})

        logging.info(f"Found {len(results)} announcements for KSEAB.")

    except Exception as e:
        # Improved error logging with full exception details
        error_type = type(e).__name__
        error_msg = str(e) if str(e) else f"{error_type} occurred"
        logging.error(f"An error occurred while scraping KSEAB: {error_type}: {error_msg}", exc_info=True)
        try:
            driver.save_screenshot('kseab_error.png')
        except Exception as screenshot_error:
            logging.error(f"Failed to save screenshot: {screenshot_error}")

    return results