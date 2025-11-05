import os
import psycopg2
from psycopg2 import extras
from enum import Enum
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from dotenv import load_dotenv

# --- Load environment variables from .env ---
load_dotenv()

# --- FastAPI App Initialization ---
app = FastAPI(title="GETNOTIFY Scraper API", version="2.0")

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(filename)s] - %(message)s"
)

# --- CORS Configuration ---
origins = [
    "http://localhost:5173",
    "http://localhost:8501",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# --- Enum for Supported Sources ---
class SourceEnum(str, Enum):
    mahacet = "MAHACET"
    nta = "NTA"
    cbse = "CBSE"
    neet = "NEET"
    jee = "JEE"
    gate = "GATE"
    upsc = "UPSC"
    mpsc = "MPSC"
    rrbmumbai = "RRBMumbai"
    isro = "ISRO"
    rrbkolkata = "RRBKolkata"
    rrbahmedabad = "RRBAhmedabad"
    kseab = "KSEAB"
    kea = "KEA"


# --- Database Connection Helper ---
def get_db_connection():
    """Establishes a connection to Supabase PostgreSQL database."""
    conn_params = {
        "host": os.getenv("DB_HOST", "db.hfsazlirxtjbarftyqqh.supabase.co"),
        "dbname": os.getenv("DB_NAME", "postgres"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "Pratham@123"),
        "port": os.getenv("DB_PORT", "5432"),
        "sslmode": "require"
    }
    try:
        conn = psycopg2.connect(**conn_params)
        return conn
    except psycopg2.Error as e:
        logging.error(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")


# --- Root Route ---
@app.get("/")
async def root():
    return {"message": "GETNOTIFY Scraper API is running successfully 🚀"}


# --- API: Get All Available Sources ---
@app.get("/sources")
async def get_sources():
    """
    Returns a list of all unique exam sources stored in Supabase.
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    try:
        cursor.execute("SELECT DISTINCT source FROM announcements ORDER BY source ASC")
        sources = [row['source'] for row in cursor.fetchall()]
        return {"sources": sources}
    except Exception as e:
        logging.error(f"Error fetching sources: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch sources")
    finally:
        cursor.close()
        conn.close()


# --- API: Get Announcements for a Source ---
@app.get("/announcements/{source}")
async def get_source_data(source: SourceEnum):
    """
    Fetches all announcements for a given source from Supabase.
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    try:
        cursor.execute("""
            SELECT id, source, text, link, scraped_at
            FROM announcements
            WHERE source = %s
            ORDER BY id DESC
        """, (source.value,))
        results = cursor.fetchall()
        return {"source": source.value, "data": results}
    except Exception as e:
        logging.error(f"Error fetching announcements for {source}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch announcements for {source}")
    finally:
        cursor.close()
        conn.close()


# --- API: Latest News ---
@app.get("/latest-news")
async def get_latest_news():
    """
    Fetches the latest news from the latest_news table in Supabase.
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    try:
        cursor.execute("""
            SELECT headline, article_link, article_date
            FROM latest_news
            ORDER BY scraped_at DESC
        """)
        news = cursor.fetchall()
        return {"news": news}
    except Exception as e:
        logging.error(f"Error fetching latest news: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch latest news")
    finally:
        cursor.close()
        conn.close()


# --- Health Check Endpoint ---
@app.get("/health")
async def health_check():
    """
    Verifies database connection and API health.
    """
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "healthy", "db_connection": "ok"}
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}


# --- Run Command ---
# Run this API using: uvicorn scraper_api:app --reload --port 8000
