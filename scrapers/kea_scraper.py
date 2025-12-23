import logging
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import time

def scrape(driver):
    """
    Scrapes the KEA announcements by finding the parent container first.
    This version scrapes the default language of the site.
    """
    logging.info("Scraping KEA website by finding the parent 'card-body' container.")
    results = []

    try:
        # Increased wait time to 60 seconds for slow page loads and connection issues
        wait = WebDriverWait(driver, 60)

        # 1. Wait for the parent div with class 'card-body pt-6' to be visible.
        parent_div_selector = (By.CSS_SELECTOR, "div.card-body.pt-6")
        wait.until(EC.visibility_of_element_located(parent_div_selector))
        time.sleep(2) # Pause to ensure content inside is stable

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 2. Find that specific parent div in the parsed HTML.
        parent_div = soup.find('div', class_='card-body pt-6')
        if not parent_div:
            logging.error("KEA: Could not find the parent div (div.card-body.pt-6).")
            return []

        # 3. NOW, look for the table *only inside* that parent div.
        table_id = "ContentPlaceHolder1_Gridlatestannoc"
        announcement_table = parent_div.find('table', id=table_id)

        if not announcement_table:
            logging.error(f"KEA: Could not find table with ID '{table_id}' inside the parent div.")
            return []

        announcement_links = announcement_table.find_all('a')
        if not announcement_links:
            logging.warning("KEA: No announcement links were found within the table.")
            return []

        for link_tag in announcement_links:
            if link_tag and link_tag.has_attr('href'):
                text = link_tag.get_text(strip=True)
                link = urljoin(driver.current_url, link_tag['href'])
                if text and link:
                    results.append({"text": text, "link": link})

        logging.info(f"Found {len(results)} announcements for KEA.")

    except Exception as e:
        logging.error(f"An error occurred while scraping KEA: {e}", exc_info=False)
        driver.save_screenshot('kea_error.png')
        
    return results