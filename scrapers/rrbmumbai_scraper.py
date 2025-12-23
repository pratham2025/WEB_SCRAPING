import logging
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import time

def scrape(driver):
    """Scrapes the RRB Mumbai 'Important Message' table."""
    logging.info("Scraping RRB Mumbai (important.php) website.")
    results = []

    try:
        # Increased wait time from 20 to 60 seconds for slow page loads and connection issues
        wait = WebDriverWait(driver, 60)
        # Wait for the table to be present on the page. This is our reliable target.
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-bordered")))
        time.sleep(2)  # Increased from 1 to 2 seconds for page stability

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the table and then all the rows in its body
        announcement_table = soup.find('table', class_='table-bordered')
        table_rows = announcement_table.find('tbody').find_all('tr')

        if not table_rows:
            logging.warning("RRB Mumbai: Found the table but it has no rows.")
            return []

        for row in table_rows:
            # Find all cells (td) in the current row
            cells = row.find_all('td')
            
            # Ensure the row has the expected number of cells (at least 3)
            if len(cells) >= 3:
                cen_details = cells[0].get_text(strip=True)
                subject_cell = cells[1]
                
                subject_text = subject_cell.get_text(strip=True)
                link_tag = subject_cell.find('a')
                
                # Create a descriptive text for the announcement
                full_text = f"{cen_details} | {subject_text}"
                
                # Get the link if it exists, otherwise use a placeholder
                if link_tag and link_tag.has_attr('href'):
                    link = urljoin(driver.current_url, link_tag['href'])
                else:
                    link = f"#{cen_details.replace(' ', '-')}" # Placeholder
                
                results.append({"text": full_text, "link": link})

        logging.info(f"Found {len(results)} announcements for RRB Mumbai.")

    except Exception as e:
        logging.error(f"An error occurred while scraping RRB Mumbai: {e}", exc_info=True)

    return results