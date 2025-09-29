import logging
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import time

def scrape(driver):
    """Scrapes the ISRO Careers page using the undetected driver."""
    logging.info("Scraping ISRO Careers page with an undetected driver.")
    results = []

    try:
        wait = WebDriverWait(driver, 20)

        # Wait for the tbody with class='list', as you identified.
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody.list")))
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Find the table body directly
        table_body = soup.find('tbody', class_='list')
        
        if not table_body:
            logging.error("ISRO: tbody.list not found even with undetected driver.")
            return []

        # Find all rows within that body
        announcement_items = table_body.find_all('tr')
        
        for item in announcement_items:
            # Find the cell with class='news'
            news_cell = item.find('td', class_='news')
            if news_cell:
                link_tag = news_cell.find('a')
                if link_tag:
                    text = link_tag.get_text(strip=True)
                    link = urljoin(driver.current_url, link_tag.get('href', '#'))
                    if text and link:
                        results.append({"text": text, "link": link})

        logging.info(f"Found {len(results)} announcements for ISRO.")

    except Exception as e:
        logging.error(f"An error occurred while scraping ISRO: {e}", exc_info=False)
        driver.save_screenshot('isro_final_error.png')
        
    return results