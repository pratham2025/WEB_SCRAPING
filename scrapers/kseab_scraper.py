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
        wait = WebDriverWait(driver, 20)
        # Wait for the unique container with id='newsTicker10' to be visible.
        wait.until(EC.visibility_of_element_located((By.ID, "newsTicker10")))
        time.sleep(1) 

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
        logging.error(f"An error occurred while scraping KSEAB: {e}", exc_info=False)
        driver.save_screenshot('kseab_error.png')

    return results