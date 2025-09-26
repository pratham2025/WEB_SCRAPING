import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def scrape(driver):
    """Scrapes the MPSC advertisements page using Selenium."""
    logging.info("Scraping MPSC advertisements page.")
    results = []
    try:
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.ID, "datatable")))
        time.sleep(2)
        rows = driver.find_elements(By.CSS_SELECTOR, "#datatable tbody tr")
        seen_texts = set()
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 5:
                continue
            adv_no = cols[1].text.strip()
            subject_text = cols[2].text.strip()
            pub_date = cols[3].text.strip()
            try:
                pdf_tag = cols[4].find_element(By.TAG_NAME, "a")
                pdf_link = pdf_tag.get_attribute("href")
            except:
                pdf_link = None
            if not subject_text:
                continue
            clean_text = f"{adv_no} | {subject_text} | {pub_date}".replace('\n', ' ').strip()
            if clean_text in seen_texts:
                continue
            seen_texts.add(clean_text)
            link = pdf_link if pdf_link else f"#{adv_no}-{pub_date}"
            results.append({"text": clean_text, "link": link})
    except TimeoutException:
        logging.error("MPSC: Timed out waiting for table.")
        driver.save_screenshot("mpsc_error_screenshot.png")
    except Exception as e:
        logging.error(f"MPSC: Unexpected error - {e}")
    logging.info(f"Found {len(results)} announcements for MPSC.")
    return results