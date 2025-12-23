import logging
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape(driver):
    """Scrapes the MAHACET website."""
    logging.info("Scraping MAHACET website.")
    # Increased wait time to 60 seconds for slow page loads and connection issues
    wait = WebDriverWait(driver, 60)
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