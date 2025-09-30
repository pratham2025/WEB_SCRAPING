# ExamDoor 🔔 Educational Announcements Aggregator

A comprehensive full-stack project for automated scraping, aggregating, and browsing announcements from major Indian educational websites. The system features parallel scraping of 12+ official portals, PostgreSQL database storage with deduplication, REST API, and multiple modern interfaces for users.

---

## Features
- **Automated Parallel Scraping**: Concurrent scraping of 12+ educational portals using Selenium + BeautifulSoup
- **Robust Database**: PostgreSQL with deduplication and conflict resolution
- **REST API**: FastAPI backend with CORS support for announcements and sources
- **Modern Web UI**: Glassdoor-inspired responsive interface with search, filtering, and pagination
- **Streamlit Dashboard**: Interactive data exploration with dynamic tab creation
- **Docker Support**: Complete containerization with PostgreSQL database
- **Configurable Sources**: Easy source management via `config.json`
- **Comprehensive Logging**: Detailed monitoring for scraping operations and errors
- **Anti-Detection**: Undetected Chrome WebDriver to bypass bot protection

---

## Supported Educational Sources
- **MAHACET** - Maharashtra Common Entrance Test
- **NTA** - National Testing Agency
- **CBSE** - Central Board of Secondary Education
- **NEET** - National Eligibility cum Entrance Test
- **JEE** - Joint Entrance Examination
- **GATE** - Graduate Aptitude Test in Engineering
- **UPSC** - Union Public Service Commission
- **MPSC** - Maharashtra Public Service Commission
- **RRB Mumbai** - Railway Recruitment Board Mumbai
- **RRB Kolkata** - Railway Recruitment Board Kolkata
- **RRB Ahmedabad** - Railway Recruitment Board Ahmedabad
- **ISRO** - Indian Space Research Organisation

---

## Requirements
- Python 3.10+
- Google Chrome browser
- ChromeDriver (auto-managed by webdriver-manager)
- PostgreSQL 15+ (local or Docker)
- See `requirements.txt` for Python dependencies

---

## Project Structure
```
WEB_SCRAPING/
├── worker.py                 # Main parallel scraping orchestrator
├── scraper_api.py           # FastAPI backend with CORS support
├── frontend/
│   ├── app.py              # Streamlit dashboard
│   ├── index.html          # Modern web UI (main interface)
│   ├── app.js              # Frontend JavaScript with API integration
│   ├── styles.css          # Glassdoor-inspired responsive styling
│   ├── home.html           # Landing page
│   └── syllabus.html       # Syllabus information page
├── scrapers/               # Individual scraper modules
│   ├── mahacet_scraper.py  # MAHACET announcements
│   ├── nta_scraper.py      # NTA notifications
│   ├── cbse_scraper.py     # CBSE circulars
│   ├── neet_scraper.py     # NEET announcements
│   ├── jee_scraper.py      # JEE notifications
│   ├── gate_scraper.py     # GATE notifications
│   ├── upsc_scraper.py     # UPSC notifications
│   ├── mpsc_scraper.py     # MPSC announcements
│   ├── rrbmumbai_scraper.py # RRB Mumbai notices
│   ├── rrbkolkata_scraper.py # RRB Kolkata notices
│   ├── rrbahmedabad_scraper.py # RRB Ahmedabad notices
│   └── isro_scraper.py     # ISRO career notifications
├── config.json             # Source configuration
├── requirements.txt        # Python dependencies
├── dockerfile             # Container configuration
├── docker-compose.yml     # Multi-service Docker setup
├── init_db.py            # Legacy SQLite initializer
└── web_scrape.py         # Standalone scraper example
```

---

## Step-by-Step Setup & Usage

### 1. Clone the repository
```sh
git clone https://github.com/pratham2025/WEB_SCRAPING.git
cd WEB_SCRAPING
```

### 2. Install Python dependencies
```sh
pip install -r requirements.txt
```

### 3. Set up PostgreSQL database
- **Option 1: Docker (recommended):**
  ```sh
  docker-compose up -d
  ```
- **Option 2: Manual:**
  - Install PostgreSQL 15+.
  - Create a database named `announcements_db` and user `notifyme` with password `Pratham@2025`.
  - Update credentials in `scraper_api.py` and `worker.py` if needed.

### 4. Configure scraping sources
- Edit `config.json` to add/remove sources and URLs as needed.
- Currently configured sources: MAHACET, NTA, CBSE, NEET, JEE, GATE, UPSC, MPSC, RRB Mumbai, RRB Kolkata, RRB Ahmedabad, ISRO

---

## Running the Project

### 1. Run the scraping worker
This will scrape all configured sources in parallel and update the PostgreSQL database every hour.
```sh
python worker.py
```

### 2. Start the FastAPI backend
This serves the announcements and sources via REST API with CORS enabled.
```sh
uvicorn scraper_api:app --reload --host 127.0.0.1 --port 8000
```

### 3. Launch the Streamlit dashboard
This provides an interactive dashboard for browsing announcements with dynamic tab creation.
```sh
streamlit run frontend/app.py
```

### 4. Use the Modern Web UI
- **Static Preview**: Open `frontend/index.html` directly in your browser
- **Dynamic Experience**: 
  1. Serve the frontend using a local server (e.g., VS Code Live Server, Python's `http.server`)
  2. Ensure the FastAPI backend is running
  3. Open `http://127.0.0.1:5500/frontend/index.html` in your browser

---

## API Endpoints

### GET /sources
Returns all available sources that have data in the database.
```json
{
  "sources": ["CBSE", "JEE", "MAHACET", "NEET", "NTA", ...]
}
```

### GET /announcements/{source}
Returns announcements for a specific source.
```json
{
  "source": "CBSE",
  "data": [
    {
      "id": 1,
      "source": "CBSE",
      "text": "Announcement title",
      "link": "https://example.com/announcement"
    }
  ]
}
```

---

## Docker Deployment

### Using Docker Compose (Recommended)
```sh
# Start PostgreSQL database
docker-compose up -d

# Build and run the application
docker build -t examdoor .
docker run -p 8000:8000 --network host examdoor
```

### Environment Configuration
Update `docker-compose.yml` with your preferred database credentials:
```yaml
environment:
  POSTGRES_USER: your_db_user
  POSTGRES_PASSWORD: your_db_password
  POSTGRES_DB: announcements_db
```

---

## Adding New Sources

### 1. Update Configuration
Add a new entry in `config.json`:
```json
{
  "name": "NEW_SOURCE",
  "url": "https://example.com/notifications"
}
```

### 2. Create Scraper Module
Create `scrapers/new_source_scraper.py`:
```python
import logging
from bs4 import BeautifulSoup

def scrape(driver):
    """Scrapes the NEW_SOURCE website."""
    logging.info("Scraping NEW_SOURCE website.")
    # Your scraping logic here
    results = []
    # ... scraping implementation
    return results
```

### 3. Update API Enum
Add the new source to `SourceEnum` in `scraper_api.py`:
```python
class SourceEnum(str, Enum):
    # ... existing sources
    newsource = "NEW_SOURCE"
```

---

## Technical Details

### Scraping Architecture
- **Parallel Processing**: Uses ThreadPoolExecutor with max 10 workers
- **Anti-Detection**: Undetected Chrome WebDriver with stealth options
- **Error Handling**: Graceful fallback mechanisms for failed scrapes
- **Deduplication**: Database-level conflict resolution prevents duplicates

### Database Schema
```sql
CREATE TABLE announcements (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL,
    text TEXT NOT NULL,
    link TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source, text)
);
```

### Performance Features
- **Caching**: Streamlit dashboard caches API responses for 10 minutes
- **Pagination**: Web UI supports pagination for large result sets
- **Search & Filter**: Real-time search and source filtering
- **Responsive Design**: Mobile-friendly interface with modern styling

---

## Troubleshooting

### Common Issues

1. **Chrome Driver Issues**
   - Ensure Google Chrome is installed
   - ChromeDriver is auto-managed by webdriver-manager

2. **Database Connection Errors**
   - Verify PostgreSQL is running
   - Check credentials in `scraper_api.py` and `worker.py`
   - Ensure database `announcements_db` exists

3. **CORS Errors in Web UI**
   - FastAPI CORS is configured for common localhost ports
   - Serve frontend from `127.0.0.1:5500` or similar

4. **Scraping Failures**
   - Check website structure changes
   - Review logs for specific error messages
   - Some sites may block automated requests

### Logs
All components include comprehensive logging:
- Worker: Scraping progress and database operations
- API: Request handling and database connections
- Streamlit: Data fetching and caching

---

## License
MIT License

## Author
[pratham2025](https://github.com/pratham2025)

---

**Tip**: For best results, run the backend (FastAPI) and database (PostgreSQL) before using the web or Streamlit UIs. The system is designed to handle high-volume scraping with automatic retry mechanisms and graceful error handling.