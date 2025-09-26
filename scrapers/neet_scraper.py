import logging
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape(driver):
    """Scrapes the NEET website."""
    logging.info("Scraping NEET website.")
    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".wpb_wrapper ul li a")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = []
    notice_list = soup.select_one(".wpb_wrapper ul")
    if notice_list:
        for item in notice_list.find_all('li'):
            link_tag = item.find('a')
            if link_tag and link_tag.text.strip():
                text = link_tag.text.strip()
                link = link_tag.get('href', '#')
                if not link.startswith('http'):
                    link = urljoin(driver.current_url, link)
                results.append({"text": text, "link": link})
    logging.info(f"Found {len(results)} announcements for NEET.")
    return results