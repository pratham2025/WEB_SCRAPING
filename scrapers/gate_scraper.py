import logging
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def scrape(driver):
    """Scrapes announcements from the GATE website."""
    logging.info("Scraping GATE website.")
    results = []
    try:
        # Increased wait time to 60 seconds for slow page loads and connection issues
        wait = WebDriverWait(driver, 60)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-bordered")))
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        notification_table = soup.find('table', class_='table-bordered')
        if not notification_table:
            logging.warning("GATE: Could not find the notification table.")
            return []
        for row in notification_table.find_all('tr'):
            cell = row.find('td', class_='text-left')
            if not cell:
                continue
            text = cell.get_text(strip=True)
            link_tag = cell.find('a')
            if link_tag and link_tag.get('href', '#') != '#':
                link = link_tag.get('href')
            else:
                placeholder = text.replace(' ', '-').replace('.', '')
                link = f"#{placeholder}"
            if text:
                if not link.startswith('http') and not link.startswith('#'):
                    link = urljoin(driver.current_url, link)
                results.append({"text": text, "link": link})
    except TimeoutException:
        logging.error("GATE: Timed out waiting for the notifications table to load.")
    except Exception as e:
        logging.error(f"An unexpected error occurred while scraping GATE: {e}")
    logging.info(f"Found {len(results)} announcements for GATE.")
    return results