# scraper_api.py (Updated to include Summaries)

import psycopg2
from psycopg2 import extras
from enum import Enum
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(filename)s] - %(message)s')


# --- CORS Configuration ---
origins = [
    "http://localhost:5173",
    "http://localhost:8501",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# --- Source Enum (No changes needed) ---
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


# --- Helper Functions (No changes needed) ---
def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    conn_params = {
        "host": "localhost",
        "dbname": "announcements_db",
        "user": "notifyme",
        "password": "Pratham@2025",
        "port": "5432"
    }
    try:
        conn = psycopg2.connect(**conn_params)
        return conn
    except psycopg2.Error as e:
        logging.error(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

# --- API Endpoints ---

@app.get("/sources")
async def get_sources():
    """
    Dynamically discovers and returns a list of all unique sources
    that have data in the announcements table.
    """
    conn = get_db_connection()
    # Using RealDictCursor allows us to access columns by name easily
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor) 
    cursor.execute("SELECT DISTINCT source FROM announcements ORDER BY source ASC")
    sources = [row['source'] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return {"sources": sources}


@app.get("/announcements/{source}")
async def get_source_data(source: SourceEnum):
    """
    Fetches announcement data, including the new summary, for a specified source.
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    
    # --- MODIFIED: Added the 'summary' column to the SELECT statement ---
    sql_select_query = """
        SELECT id, source, text, link, summary 
        FROM announcements 
        WHERE source = %s 
        ORDER BY id DESC
    """
    
    cursor.execute(sql_select_query, (source.value,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return {"source": source.value, "data": results}