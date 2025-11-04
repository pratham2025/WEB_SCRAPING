import logging
import psycopg2
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Database Functions ---

def clear_old_news(conn_params):
    """Deletes all existing rows from the latest_news table."""
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE latest_news RESTART IDENTITY;")
        conn.commit()
        logging.info("Successfully truncated latest_news table.")
    except Exception as e:
        logging.error(f"Error truncating news table: {e}")
    finally:
        if conn: conn.close()

def insert_new_news(conn_params, news_items):
    """Inserts a list of new news items into the database."""
    if not news_items:
        logging.info("No new news items to insert.")
        return

    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO latest_news (headline, article_link, article_date)
        VALUES (%s, %s, %s)
        ON CONFLICT (article_link) DO NOTHING
        """
        
        for item in news_items:
            cursor.execute(insert_query, (item['headline'], item['link'], item['date']))
            
        conn.commit()
        logging.info(f"Successfully inserted {len(news_items)} new news items.")
    except Exception as e:
        logging.error(f"Error inserting new news: {e}")
    finally:
        if conn: conn.close()

# --- Main Scraper Function ---
def scrape(driver):
    """
    Scrapes the Indian Express education page using Selenium.
    """
    logging.info("Scraping Indian Express (Headline/Date only)...")
    results = []
    
    conn_params = {
        "host": "localhost",
        "dbname": "announcements_db",
        "user": "notifyme",
        "password": "Pratham@2025",
        "port": "5432"
    }
    
    try:
        wait = WebDriverWait(driver, 20)
        # We still wait for the "div.articles" container
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.articles")))
        time.sleep(1) 

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # We can find all articles inside the 'leftpanel' for precision
        left_panel = soup.find('div', class_='leftpanel')
        if not left_panel:
            logging.error("Indian Express: Could not find 'div.leftpanel'.")
            return []

        articles = left_panel.find_all("div", class_="articles")
        if not articles:
            logging.warning("Indian Express: No articles found inside 'leftpanel'.")
            return []

        for article in articles:
            headline, link, date = "", "", ""
            context_div = article.find('div', class_='img-context')
            if context_div:
                
                # --- THE FIX: Changed 'h3' to 'h2' ---
                title_tag = context_div.find('h2', class_='title')
                
                if title_tag:
                    link_tag = title_tag.find('a')
                    if link_tag:
                        headline = link_tag.get_text(strip=True)
                        link = urljoin(driver.current_url, link_tag['href'])

                date_tag = context_div.find('div', class_='date')
                if date_tag:
                    date = date_tag.get_text(strip=True)

            if headline and link:
                results.append({
                    "headline": headline,
                    "link": link,
                    "date": date
                })
        
        logging.info(f"Found {len(results)} news articles from Indian Express.")

        if results:
            clear_old_news(conn_params)
            insert_new_news(conn_params, results)
        else:
            logging.warning("No news articles found for Indian Express.")
        
        return []

    except Exception as e:
        logging.error(f"An error occurred while scraping Indian Express: {e}", exc_info=False)
        driver.save_screenshot('indianexpress_error.png')
        return []