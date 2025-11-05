import logging
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from supabase import create_client
from dotenv import load_dotenv
import os

# Load Supabase credentials
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def scrape(driver):
    """
    Scrapes the Indian Express education page and stores the results in 'latest_news' table.
    """
    logging.info("Scraping Indian Express (Headline/Date only)...")
    results = []

    try:
        wait = WebDriverWait(driver, 25)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.articles")))
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        left_panel = soup.find("div", class_="leftpanel")
        if not left_panel:
            logging.error("Indian Express: Could not find 'div.leftpanel'.")
            return []

        articles = left_panel.find_all("div", class_="articles")
        if not articles:
            logging.warning("Indian Express: No articles found inside 'leftpanel'.")
            return []

        for article in articles:
            headline, link, date = "", "", ""
            context_div = article.find("div", class_="img-context")
            if context_div:
                title_tag = context_div.find("h2", class_="title")
                if title_tag:
                    link_tag = title_tag.find("a")
                    if link_tag:
                        headline = link_tag.get_text(strip=True)
                        link = urljoin(driver.current_url, link_tag["href"])

                date_tag = context_div.find("div", class_="date")
                if date_tag:
                    date = date_tag.get_text(strip=True)

            if headline and link:
                results.append({
                    "headline": headline,
                    "article_link": link,
                    "article_date": date
                })

        logging.info(f"Found {len(results)} news articles from Indian Express.")

        # --- Save to Supabase ---
        new_items = 0
        for item in results:
            headline = item["headline"]
            link = item["article_link"]

            # check if article already exists
            existing = supabase.table("latest_news").select("id").eq("article_link", link).execute()
            if not existing.data:
                supabase.table("latest_news").insert({
                    "headline": headline,
                    "article_link": link,
                    "article_date": item["article_date"],
                    "scraped_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                }).execute()
                new_items += 1

        logging.info(f"✅ Supabase DB: Added {new_items} new news articles to 'latest_news'.")
        return results

    except Exception as e:
        logging.error(f"An error occurred while scraping Indian Express: {e}", exc_info=False)
        driver.save_screenshot("indianexpress_error.png")
        return []
