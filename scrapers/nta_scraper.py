import logging
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape(driver):
    """Scrapes the NTA website."""
    logging.info("Scraping NTA website.")
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'latestPart')))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = []
    notice_box = soup.find('marquee', class_='latestPart')
    if notice_box:
        for item in notice_box.find_all('p'):
            text_tag = item.find('content')
            link_tag = item.find('a')
            if text_tag and link_tag and text_tag.text.strip():
                link = link_tag.get('href', '#')
                if not link.startswith('http'):
                    link = urljoin("https://www.nta.ac.in/", link)
                results.append({"text": text_tag.text.strip(), "link": link})
    logging.info(f"Found {len(results)} announcements for NTA.")
    return results