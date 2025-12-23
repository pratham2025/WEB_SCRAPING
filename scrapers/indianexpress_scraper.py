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
    Scrapes the Indian Express education page (headline, link, date, image).
    """
    logging.info("Scraping Indian Express (Education News)…")
    results = []

    try:
        # Increased wait time from 25 to 60 seconds for slow page loads
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.articles"))
        )
        time.sleep(3)  # Increased from 1 to 3 seconds for page stability

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # ---- Correct selector for article blocks ----
        articles = soup.select("div.articles")

        if not articles:
            logging.warning("No articles found inside Indian Express education section.")
            return []

        for article in articles:
            headline = ""
            link = ""
            date = ""
            image_url = ""

            # --------------- IMAGE (Correct Selector) ----------------
            img_tag = article.select_one("div.snaps a img")

            if img_tag:
                image_url = (
                    img_tag.get("data-src")
                    or img_tag.get("data-lazy-src")
                    or img_tag.get("data-srcset")
                    or img_tag.get("srcset")
                    or img_tag.get("src")
                    or ""
                )

            # If srcset contains multiple URLs → choose the first one
            if image_url and " " in image_url:
                image_url = image_url.split(" ")[0]

            if image_url:
                image_url = urljoin(driver.current_url, image_url)

            # Debug log (optional)
            logging.info(f"IMAGE FOUND: {image_url}")

            # ---------------- TITLE + LINK ----------------
            title_tag = article.select_one("div.img-context h2.title a")
            if title_tag:
                headline = title_tag.get_text(strip=True)
                link = urljoin(driver.current_url, title_tag.get("href", ""))

            # ---------------- DATE ----------------
            date_tag = article.select_one("div.img-context div.date")
            if date_tag:
                date = date_tag.get_text(strip=True)

            # Add only if headline & link exist
            if headline and link:
                results.append({
                    "headline": headline,
                    "article_link": link,
                    "article_date": date,
                    "image_url": image_url
                })

        logging.info(f"Found {len(results)} news articles from Indian Express.")

        # --------------- Save into Supabase ----------------
        new_items = 0
        for item in results:

            exists = supabase.table("latest_news") \
                             .select("id") \
                             .eq("article_link", item["article_link"]) \
                             .execute()

            if not exists.data:
                supabase.table("latest_news").insert({
                    "headline": item["headline"],
                    "article_link": item["article_link"],
                    "article_date": item["article_date"],
                    "image_url": item["image_url"],
                    "scraped_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                }).execute()

                new_items += 1

        logging.info(f"Saved {new_items} new articles to Supabase latest_news.")

        return results

    except Exception as e:
        logging.error(f"[indianexpress_scraper.py] Error scraping Indian Express: {e}")
        driver.save_screenshot("indianexpress_error.png")
        return []
