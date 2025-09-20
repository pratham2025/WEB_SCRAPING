# WEB_SCRAPING

A Python project for scraping announcements from educational websites (such as MAHACET, NTA, and CBSE) and storing them in a local SQLite database. The project uses Selenium for browser automation and BeautifulSoup for HTML parsing.

## Features
- Scrapes announcements from multiple educational portals
- Stores new announcements in a SQLite database, avoiding duplicates
- Modular scraping logic for easy extension
- Headless browser operation for automation
- Logging for monitoring scraping activity and errors

## Requirements
- Python 3.7+
- Google Chrome browser
- ChromeDriver (auto-managed by webdriver-manager)
- See `requirements.txt` for Python dependencies

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/pratham2025/WEB_SCRAPING.git
   cd WEB_SCRAPING
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```sh
   python init_db.py
   ```

## Usage
To run the scraping worker:
```sh
python worker.py
```
This will scrape the configured websites and update the `data.db` database with new announcements.

## Project Structure
- `worker.py` - Main scraping logic
- `init_db.py` - Initializes the SQLite database
- `scraper_api.py` - (Optional) API for accessing scraped data
- `app.py` - (Optional) Application entry point or web server
- `requirements.txt` - Python dependencies
- `dockerfile` - Docker containerization instructions
- `config.json` - Configuration file (if used)

## Adding New Sources
To add a new website to scrape:
- Add a new `elif` block in the `scrape_and_save` function in `worker.py` with the scraping logic for the new source.
- Add the new source to the list of sites in the `__main__` section of `worker.py`.

## License
MIT License

## Author
[pratham2025](https://github.com/pratham2025)
