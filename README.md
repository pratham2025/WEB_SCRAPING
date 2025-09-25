# ExamDoor — Educational Announcements Aggregator

A full-stack project for scraping, aggregating, and browsing announcements from major educational websites (MAHACET, NTA, CBSE, NEET, JEE, GATE, etc.). The system scrapes official portals, stores announcements in a PostgreSQL database, and provides both API and modern web/Streamlit dashboards for users.

---

## Features
- Automated scraping of multiple educational portals (Selenium + BeautifulSoup)
- PostgreSQL database for robust, deduplicated storage
- REST API (FastAPI) for announcements and sources
- Modern web UI (HTML/CSS/JS) for browsing, searching, and sorting notifications
- Streamlit dashboard for interactive data exploration
- Docker support for easy deployment
- Configurable sources via `config.json`
- Logging for monitoring scraping and errors

---

## Requirements
- Python 3.7+
- Google Chrome browser
- ChromeDriver (auto-managed by webdriver-manager)
- PostgreSQL (local or Docker)
- Node.js (for static web preview, optional)
- See `requirements.txt` for Python dependencies

---

## Project Structure
- `worker.py` — Main scraping logic and database update loop
- `scraper_api.py` — FastAPI backend serving announcements and sources
- `app.py` — Streamlit dashboard for interactive browsing
- `init_db.py` — (Legacy) SQLite DB initializer (main code uses PostgreSQL)
- `web_scrape.py` — Standalone MAHACET scraper example
- `config.json` — List of sources and URLs to scrape
- `requirements.txt` — Python dependencies
- `dockerfile`, `docker-compose.yml` — Docker setup for backend and database
- `index.html`, `app.js`, `styles.css` — Modern web UI for announcements
- `home.html`, `syllabus.html` — Additional web pages

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
  - Install PostgreSQL.
  - Create a database named `announcements_db` and a user/password as in `scraper_api.py`/`worker.py`.
  - Update credentials in the code if needed.

### 4. Configure scraping sources
- Edit `config.json` to add/remove sources and URLs as needed.

---

## Running the Project

### 1. Run the scraping worker
This will scrape all configured sources and update the PostgreSQL database.
```sh
python worker.py
```

### 2. Start the FastAPI backend
This serves the announcements and sources via REST API.
```sh
uvicorn scraper_api:app --reload
```

### 3. (Optional) Launch the Streamlit dashboard
This provides an interactive dashboard for browsing announcements.
```sh
streamlit run app.py
```

### 4. (Optional) Preview the web UI
- For a static preview, open `index.html` in your browser.
- For a dynamic, API-powered experience:
  1. Serve the frontend using a local server (e.g., VS Code Live Server, Python's `http.server`, or Node's `http-server`).
  2. Ensure the FastAPI backend is running with CORS enabled.
  3. Open `http://127.0.0.1:5500/index.html` (or your server's address) in your browser.

---

## Adding New Sources
- Add a new entry in `config.json` with the source name and URL.
- Implement a new scraper function in `worker.py` and add it to the `SCRAPERS` dict.
- (Optional) Update the FastAPI/Streamlit UI if you want custom handling.

---

## License
MIT License

## Author
[pratham2025](https://github.com/pratham2025)

---

**Tip:** For best results, run the backend (FastAPI) and database (PostgreSQL) before using the web or Streamlit UIs. For static preview, open `index.html` directly, but dynamic features require the API running with CORS enabled.
