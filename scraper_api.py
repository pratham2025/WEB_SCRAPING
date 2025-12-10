# scraper_api.py — Supabase-native FastAPI Scraper API

import os
import time
import importlib
import logging
from typing import List, Dict, Any
from enum import Enum
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client

import undetected_chromedriver as uc
from selenium import webdriver

# --- Load .env ---
load_dotenv()

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - [%(filename)s] - %(message)s")

# --- FastAPI ---
app = FastAPI(title="GETNOTIFY Supabase API", version="3.0")

# --- CORS ---
origins = [
    "http://localhost:5173",
    "http://localhost:8501",
    "http://localhost:5500",
    "http://localhost:5501",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5501",
    "http://127.0.0.1:8000",
    "http://192.168.0.197:8000",
    "http://192.168.0.197:5500",
    "http://192.168.0.197:5501",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# --- Supabase Init ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("❌ Missing Supabase credentials. Please check your .env file.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
logging.info("✅ Connected to Supabase successfully")

# --- Supported sources ---
class SourceEnum(str, Enum):
    MAHACET = "MAHACET"
    NTA = "NTA"
    CBSE = "CBSE"
    NEET = "NEET"
    JEE = "JEE"
    GATE = "GATE"
    UPSC = "UPSC"
    MPSC = "MPSC"
    RRBMumbai = "RRBMumbai"
    ISRO = "ISRO"
    RRBKolkata = "RRBKolkata"
    RRBAhmedabad = "RRBAhmedabad"
    KSEAB = "KSEAB"
    KEA = "KEA"
# --- Driver setup ---
def setup_driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--disable-gpu")
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    return uc.Chrome(options=opts, use_subprocess=True)

# --- Save to Supabase ---
def save_to_supabase(source: str, data: List[Dict[str, Any]]) -> int:
    """Insert scraped data into Supabase announcements table and notify subscribers."""
    if not data:
        return 0
    inserted = 0
    new_announcements = []
    try:
        for item in data:
            # set scraped_at to provided value OR current UTC time
            scraped_at = item.get("scraped_at")
            if not scraped_at:
                # ISO 8601 UTC timestamp
                scraped_at = datetime.now(timezone.utc).isoformat()

            payload = {
                "source": source,
                "text": item.get("text") or item.get("headline", ""),
                "link": item.get("link") or item.get("article_link", ""),
                "scraped_at": scraped_at
            }

            # check duplicate by source + text
            exists = supabase.table("announcements") \
                .select("id") \
                .eq("source", source) \
                .eq("text", payload["text"]) \
                .limit(1) \
                .execute()

            if not exists.data:
                supabase.table("announcements").insert(payload).execute()
                inserted += 1
                # Track new announcements for email notifications
                new_announcements.append(payload)

        logging.info(f"✅ Supabase DB updated for {source}: inserted {inserted} new records.")
        
        # Notify subscribers if there are new announcements
        if new_announcements:
            try:
                from notify_subscribers import notify_subscribers
                emails_sent = notify_subscribers(source, new_announcements)
                if emails_sent > 0:
                    logging.info(f"📧 Sent email notifications to {emails_sent} subscribers for {source}")
            except Exception as e:
                logging.error(f"❌ Failed to notify subscribers for {source}: {e}")
                # Don't fail the entire scrape if email notification fails
                
    except Exception as e:
        logging.error(f"❌ Supabase insert failed for {source}: {e}")
    return inserted

# --- Run scraper ---
def run_scraper(source_name: str):
    """Runs a single scraper module (requests or Selenium)."""
    result = {"source": source_name, "found": 0, "inserted": 0, "error": None}

    module_name = f"scrapers.{source_name.lower()}_scraper"
    logging.info(f"▶️ Running scraper for {source_name}")
    try:
        scraper = importlib.import_module(module_name)
    except ModuleNotFoundError:
        result["error"] = f"Scraper not found: {module_name}"
        return result

    driver = None
    data = []
    try:
        if hasattr(scraper, "scrape_requests"):
            data = scraper.scrape_requests()
        elif hasattr(scraper, "scrape"):
            driver = setup_driver()
            data = scraper.scrape(driver)
        else:
            raise Exception("Scraper must define scrape() or scrape_requests()")

        result["found"] = len(data)
        result["inserted"] = save_to_supabase(source_name, data)
    except Exception as e:
        logging.exception(f"Error scraping {source_name}: {e}")
        result["error"] = str(e)
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
    return result

# --- Endpoints ---

@app.get("/")
async def root():
    return {"message": "GETNOTIFY Supabase API running 🚀"}

@app.get("/sources")
async def get_sources():
    """Return all supported sources"""
    return {"sources": [s.value for s in SourceEnum]}

# ✅ FIXED: Fetch announcements in same order as ID (ascending)
@app.get("/announcements/{source}")
async def get_announcements(source: SourceEnum):
    """Fetch announcements directly from Supabase in ID ASC order (same as dashboard)."""
    try:
        # Build the query in one expression to avoid accidental line-continuation issues.
        res = (
            supabase.table("announcements")
            .select("*")
            .eq("source", source.value)
            .order("scraped_at", desc=False)  # ASC order by ID
            .limit(100)
            .execute()
        )

        return {"source": source.value, "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supabase fetch failed: {e}")

@app.get("/latest-news")
async def get_latest_news(limit: int = 100):
    """Fetch news from Supabase latest_news table (latest first).
    
    Returns fields: id, headline, article_link, article_date, scraped_at
    Orders by scraped_at (timestamp) for proper chronological sorting.
    Frontend will handle final sorting by article_date after parsing dates.
    """
    try:
        res = supabase.table("latest_news") \
            .select("*") \
            .order("scraped_at", desc=True) \
            .limit(limit) \
            .execute()
        
        logging.info(f"Fetched {len(res.data or [])} items from latest_news table")
        return {"news": res.data or []}
    except Exception as e:
        logging.error(f"Failed to fetch latest news from latest_news table: {e}")
        raise HTTPException(status_code=500, detail=f"Supabase fetch failed: {e}")

@app.post("/scrape/{source}")
async def scrape_source(source: SourceEnum):
    """Trigger a scraper for one source now."""
    result = await run_in_threadpool(run_scraper, source.value)
    return result

@app.post("/scrape_all")
async def scrape_all():
    """Scrape all sources sequentially."""
    results = []
    for src in SourceEnum:
        results.append(await run_in_threadpool(run_scraper, src.value))
    return {"results": results}

@app.get("/health")
async def health():
    """Check Supabase connection."""
    try:
        res = supabase.table("announcements").select("id").limit(1).execute()
        return {"status": "healthy", "supabase_connected": True, "records_found": len(res.data)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

# --- Subscription Endpoints ---

class SubscribeRequest(BaseModel):
    email: str
    source: str

@app.post("/subscribe")
async def subscribe(request: SubscribeRequest):
    """Subscribe a user (email) to a source for email notifications."""
    try:
        email = request.email
        source = request.source
        
        # Check if subscription already exists
        existing = supabase.table("subscriptions") \
            .select("id") \
            .eq("email", email) \
            .eq("source", source) \
            .limit(1) \
            .execute()
        
        if existing.data:
            return {"message": "Already subscribed", "subscribed": True}
        
        # Create new subscription
        supabase.table("subscriptions").insert({
            "email": email,
            "source": source,
            "created_at": datetime.now(timezone.utc).isoformat()
        }).execute()
        
        logging.info(f"✅ New subscription: {email} -> {source}")
        return {"message": "Subscribed successfully", "subscribed": True}
    except Exception as e:
        logging.error(f"❌ Subscription failed: {e}")
        raise HTTPException(status_code=500, detail=f"Subscription failed: {e}")

@app.post("/unsubscribe")
async def unsubscribe(request: SubscribeRequest):
    """Unsubscribe a user (email) from a source."""
    try:
        email = request.email
        source = request.source
        
        # Delete subscription
        supabase.table("subscriptions") \
            .delete() \
            .eq("email", email) \
            .eq("source", source) \
            .execute()
        
        logging.info(f"✅ Unsubscribed: {email} -> {source}")
        return {"message": "Unsubscribed successfully", "subscribed": False}
    except Exception as e:
        logging.error(f"❌ Unsubscribe failed: {e}")
        raise HTTPException(status_code=500, detail=f"Unsubscribe failed: {e}")

@app.get("/subscriptions")
async def get_subscriptions(email: str = None):
    """Get all subscriptions for a user (email)."""
    try:
        if not email:
            raise HTTPException(status_code=400, detail="Email parameter is required")
        
        res = supabase.table("subscriptions") \
            .select("*") \
            .eq("email", email) \
            .execute()
        
        return {"subscriptions": res.data or []}
    except Exception as e:
        logging.error(f"❌ Failed to fetch subscriptions: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch subscriptions: {e}")