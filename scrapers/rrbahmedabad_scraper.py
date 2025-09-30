import logging
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import time

def scrape(driver):
    """
    Scrapes the RRB Ahmedabad 'News Updates' page using Selenium to handle dynamic content.
    """
    logging.info("Scraping RRB Ahmedabad website using Selenium-based method.")
    # The URL is loaded by worker.py, so we don't need to call driver.get() here.
    results = []

    try:
        wait = WebDriverWait(driver, 20)
        # Wait for the first announcement block to be visible on the page
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.news-update-block")))
        time.sleep(1) # Pause to ensure all elements render

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all the div blocks that contain an individual announcement
        announcement_blocks = soup.find_all('div', class_='news-update-block shadow-block')

        if not announcement_blocks:
            logging.warning("RRB Ahmedabad: No announcement blocks were found even with Selenium.")
            return []

        for block in announcement_blocks:
            h2_tag = block.find('h2')
            if h2_tag:
                link_tag = h2_tag.find('a')
                if link_tag and link_tag.has_attr('href'):
                    text = link_tag.get_text(strip=True)
                    link = urljoin(driver.current_url, link_tag['href'])
                    if text and link:
                        results.append({"text": text, "link": link})

        logging.info(f"Found {len(results)} announcements for RRB Ahmedabad.")

    except Exception as e:
        logging.error(f"An error occurred while scraping RRB Ahmedabad: {e}", exc_info=False)
        driver.save_screenshot('rrbahmedabad_error.png')

    return results