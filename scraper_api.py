import sqlite3
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
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# --- UPDATED ENUM ---
# This tells the API which sources are valid.
class SourceEnum(str, Enum):
    mahacet = "MAHACET"
    nta = "NTA"
    cbse = "CBSE"
    neet = "NEET"
    jee = "JEE" # JEE source added back here

# --- Helper Functions ---
def dict_factory(cursor, row):
    # ... (this function is unchanged)
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def get_db_connection():
    """Establishes a connection to the database."""
    try:
        conn = sqlite3.connect("data.db")
        conn.row_factory = dict_factory
        return conn
    except sqlite3.Error as e:
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
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT source FROM announcements")
    sources = [row['source'] for row in cursor.fetchall()]
    conn.close()
    return {"sources": sources}


@app.get("/announcements/{source}")
async def get_source_data(source: SourceEnum):
    """
    Instantly fetches announcement data for a specified source from the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, source, text, link FROM announcements WHERE source = ? ORDER BY id DESC",
        (source.value,),
    )
    results = cursor.fetchall()
    conn.close()
    return {"source": source.value, "data": results}

