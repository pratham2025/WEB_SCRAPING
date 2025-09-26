import logging
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def scrape(driver):
    """Scrapes all announcements from UPSC."""
    logging.info("Scraping UPSC website.")
    results = []
    try:
        wait = WebDriverWait(driver, 20)
        target_div_selector = (By.CSS_SELECTOR, "div.scroll-content")
        wait.until(EC.presence_of_element_located(target_div_selector))
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        announcement_div = soup.find('div', class_='scroll-content')
        if not announcement_div:
            logging.warning("UPSC: Could not find the announcement container.")
            return []
        for item_span in announcement_div.find_all('span'):
            full_text = item_span.get_text(strip=True)
            if not full_text:
                continue
            link_tag = item_span.find('a')
            if link_tag:
                text = link_tag.get_text(strip=True)
                link = link_tag.get('href', '#')
            else:
                text = full_text
                placeholder = text.replace(' ', '-').replace('.', '').replace('(', '').replace(')', '')
                link = f"#{placeholder}"
            if not link.startswith('http') and not link.startswith('#'):
                link = urljoin(driver.current_url, link)
            results.append({"text": text, "link": link})
    except TimeoutException:
        logging.error("UPSC: Timed out waiting for the announcements to load.")
    except Exception as e:
        logging.error(f"An unexpected error occurred while scraping UPSC: {e}")
    logging.info(f"Found {len(results)} announcements for UPSC.")
    return results