import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape(driver):
    """
    Scrapes the RRB Kolkata employment notices page using the direct `requests` method.
    The 'driver' object is not used in this scraper.
    """
    logging.info("Scraping RRB Kolkata website using direct requests method.")
    url = "https://www.rrbkolkata.gov.in/employment_notices.php"
    results = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # --- THE FIX ---
        # The main container has an ID 'body_content', not a class.
        main_div = soup.find('div', id='body_content')
        
        if not main_div:
            logging.error("RRB Kolkata: Could not find the main content div with id='body_content'.")
            return []
            
        main_table = main_div.find('table')
        if not main_table:
            logging.error("RRB Kolkata: Could not find the announcements table.")
            return []

        table_rows = main_table.find_all('tr')
        
        for row in table_rows:
            if row.find('th') or "Employment Notice No." in row.get_text():
                continue

            cells = row.find_all('td')
            if len(cells) >= 3:
                notice_text_cell = cells[1]
                link_cell = cells[2]
                
                full_text = notice_text_cell.get_text(separator=' ', strip=True)
                
                english_link_tag = link_cell.find('a', string=lambda text: 'english version' in text.lower() if text else False)
                
                if english_link_tag and english_link_tag.has_attr('href'):
                    link = urljoin(url, english_link_tag['href'])
                    if full_text:
                         results.append({"text": full_text, "link": link})

        logging.info(f"Found {len(results)} announcements for RRB Kolkata.")

    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while fetching the RRB Kolkata page: {e}")
    except Exception as e:
        logging.error(f"An error occurred while parsing the RRB Kolkata page: {e}", exc_info=False)

    return results