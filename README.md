# 📢 GETNOTIFY — Real-time Educational Notifications Platform

🚀 **Instant Exam Alerts, Smart Scraping, and Beautiful UI for Students Across India**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)  
![Supabase](https://img.shields.io/badge/Supabase-Cloud%20Database-3ECF8E)  
![HTML5](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-blue)  
![Python](https://img.shields.io/badge/Python-3.10+-yellow)  
![Docker](https://img.shields.io/badge/Docker-Supported-2496ED)  
![Selenium](https://img.shields.io/badge/Selenium-Web%20Scraping-43B02A)

---

## 🔎 Overview

**GETNOTIFY** is a comprehensive, production-ready platform that delivers **real-time educational notifications** from official sources across India. The system automatically scrapes announcements from **15+ educational boards and organizations** including NTA, CBSE, NEET, JEE, UPSC, ISRO, KSEAB, KEA, MAHACET, MPSC, RRB boards, GATE, and Indian Express.

The platform combines:
- **FastAPI backend** with RESTful API endpoints
- **Background worker** for automated parallel web scraping
- **Supabase PostgreSQL database** for cloud storage
- **Modern responsive web UI** with Google OAuth authentication
- **Email notification system** for subscribed users
- **Modular scraper architecture** supporting multiple sources

---

## 🧠 Core Features

### Web Scraping & Data Collection
- ⚡ **Real-time Web Scraping** using Selenium and undetected_chromedriver
- 🔄 **Parallel Processing** - scrapes multiple sources simultaneously (up to 10 workers)
- 🛡️ **Anti-Detection** - uses undetected_chromedriver to avoid bot detection
- 🔍 **Duplicate Detection** - prevents storing duplicate announcements
- ⏰ **Automated Scheduling** - background worker runs every hour (configurable)
- 📊 **15+ Source Support** - extensible scraper architecture

### User Features
- 🔔 **Email Subscriptions** - users can subscribe to specific sources for email notifications
- 🔐 **Google OAuth Login** - secure authentication via Supabase Auth
- 📱 **Responsive Design** - optimized for desktop, tablet, and mobile devices
- 🎨 **Beautiful UI** - modern glass-inspired design with animations
- 📰 **Latest News Board** - pinned paper-style cards with NEW badges
- 🔍 **Source Filtering** - browse announcements by educational board
- 📄 **Pagination** - efficient browsing of large announcement lists

### Technical Features
- 🧩 **Modular Architecture** - separate scraper modules for each source
- 🗄️ **Supabase Integration** - cloud database with real-time capabilities
- 📧 **Email Notifications** - Zoho SMTP integration for sending HTML emails
- 🚀 **FastAPI REST API** - high-performance async endpoints
- 🐳 **Docker Support** - containerized deployment ready
- 📝 **Comprehensive Logging** - detailed logs for debugging and monitoring

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GETNOTIFY Platform                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────┐ │
│  │   Frontend   │◄────►│  FastAPI     │◄────►│ Supabase │ │
│  │  (HTML/JS)   │      │   Backend    │      │ Database │ │
│  └──────────────┘      └──────────────┘      └──────────┘ │
│         │                      │                    │      │
│         │                      │                    │      │
│         │              ┌───────▼────────┐          │      │
│         │              │  Worker Process │          │      │
│         │              │ (Background)    │          │      │
│         │              └───────┬────────┘          │      │
│         │                      │                    │      │
│         │         ┌───────────┴──────────┐         │      │
│         │         │                      │         │      │
│         │    ┌───▼───┐            ┌────▼────┐    │      │
│         │    │Scraper│            │Scraper  │    │      │
│         │    │  #1   │            │  #15+   │    │      │
│         │    └───────┘            └─────────┘    │      │
│         │         │                    │         │      │
│         │    ┌────▼────────────────────▼────┐   │      │
│         │    │   Educational Websites        │   │      │
│         │    │ (CBSE, JEE, NEET, UPSC...)   │   │      │
│         │    └──────────────────────────────┘   │      │
│         │                                         │      │
│         │              ┌──────────────┐          │      │
│         └─────────────►│ Email Service │◄────────┘      │
│                        │ (Zoho SMTP)  │                 │
│                        └──────────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
GETNOTIFY/
│
├── frontend/                          # Frontend application
│   ├── index.html                     # Main notifications page
│   ├── home.html                      # Homepage with notice board
│   ├── syllabus.html                  # Syllabus section
│   ├── answer_keys.html               # Answer keys section
│   ├── styles.css                     # Global styles
│   ├── app.js                         # Source & announcement logic
│   ├── home.js                        # Homepage notice board logic
│   ├── common.js                      # Header/Footer injection
│   ├── auth.js                        # Google OAuth authentication
│   ├── secrets.js                     # Supabase configuration
│   ├── _header.html                   # Reusable header component
│   ├── _footer.html                   # Reusable footer component
│   ├── privacy-policy.html            # Privacy policy page
│   ├── terms-of-use.html              # Terms of use page
│   ├── disclaimer.html                # Disclaimer page
│   ├── cookie-notice.html             # Cookie notice
│   ├── fair-use.html                  # Fair use policy
│   ├── OAUTH_SETUP.md                 # OAuth setup guide
│   └── src/
│       ├── images/                    # Image assets
│       └── logos/                     # Educational board logos
│
├── scrapers/                          # Web scraper modules
│   ├── __init__.py
│   ├── cbse_scraper.py                # CBSE announcements
│   ├── jee_scraper.py                 # JEE Main/Advanced
│   ├── neet_scraper.py                # NEET UG/PG
│   ├── nta_scraper.py                 # National Testing Agency
│   ├── gate_scraper.py                # GATE exam
│   ├── upsc_scraper.py                # UPSC civil services
│   ├── isro_scraper.py                # ISRO recruitment
│   ├── kseab_scraper.py               # Karnataka School Board
│   ├── kea_scraper.py                 # Karnataka Exams Authority
│   ├── mahacet_scraper.py             # Maharashtra CET
│   ├── mpsc_scraper.py                # Maharashtra PSC
│   ├── rrbkolkata_scraper.py          # RRB Kolkata
│   ├── rrbmumbai_scraper.py           # RRB Mumbai
│   ├── rrbahmedabad_scraper.py        # RRB Ahmedabad
│   └── indianexpress_scraper.py      # Indian Express education news
│
├── scraper_api.py                     # FastAPI REST API server
├── worker.py                          # Background worker for automated scraping
├── notify_subscribers.py              # Email notification service
├── send_email.py                      # Zoho SMTP email service
├── summarizer.py                      # AI text summarization (optional)
├── init_db.py                         # Database initialization (legacy SQLite)
├── web_scrape.py                      # Standalone scraper test script
├── test_mail.py                       # Email service test script
│
├── config.json                        # Source configuration (URLs & names)
├── requirements.txt                   # Python dependencies
├── docker-compose.yml                 # Docker Compose configuration
├── dockerfile                         # Docker image definition
├── .env                               # Environment variables (not in repo)
├── .gitignore                         # Git ignore rules
│
├── create_subscriptions_table.sql     # Supabase subscriptions table schema
├── SUBSCRIPTION_SETUP.md              # Subscription feature setup guide
├── OAUTH_SETUP.md                     # OAuth authentication setup
└── README.md                          # This file
```

---

## 🎯 Supported Educational Sources

The platform currently monitors **15+ official sources**:

| Source | Full Name | Type |
|--------|-----------|------|
| **CBSE** | Central Board of Secondary Education | School Board |
| **JEE** | Joint Entrance Examination | Engineering Entrance |
| **NEET** | National Eligibility cum Entrance Test | Medical Entrance |
| **GATE** | Graduate Aptitude Test in Engineering | Post-graduate Exam |
| **NTA** | National Testing Agency | Testing Agency |
| **UPSC** | Union Public Service Commission | Civil Services |
| **ISRO** | Indian Space Research Organisation | Recruitment |
| **KSEAB** | Karnataka School Examination and Assessment Board | State Board |
| **KEA** | Karnataka Examinations Authority | State Entrance |
| **MAHACET** | Maharashtra State CET Cell | State Entrance |
| **MPSC** | Maharashtra Public Service Commission | State PSC |
| **RRBKolkata** | Railway Recruitment Board Kolkata | Railway Recruitment |
| **RRBMumbai** | Railway Recruitment Board Mumbai | Railway Recruitment |
| **RRBAhmedabad** | Railway Recruitment Board Ahmedabad | Railway Recruitment |
| **IndianExpress** | Indian Express Education Section | News Portal |

---

## 🧾 API Endpoints

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API health check |
| `GET` | `/sources` | List all supported educational sources |
| `GET` | `/announcements/{source}` | Get announcements for a specific source |
| `GET` | `/latest-news` | Get latest educational news (from latest_news table) |
| `GET` | `/health` | Check API and database connection status |

### Subscription Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/subscribe` | Subscribe user email to a source |
| `POST` | `/unsubscribe` | Unsubscribe user email from a source |
| `GET` | `/subscriptions?email={email}` | Get all subscriptions for a user |

### Admin/Scraping Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/scrape/{source}` | Manually trigger scraper for a source |
| `POST` | `/scrape_all` | Trigger scrapers for all sources |

### Example API Responses

**Get Sources:**
```json
{
  "sources": ["CBSE", "JEE", "NEET", "NTA", "UPSC", ...]
}
```

**Get Announcements:**
```json
{
  "source": "CBSE",
  "data": [
    {
      "id": 123,
      "source": "CBSE",
      "text": "CBSE Class 12 Results 2025 Released",
      "link": "https://cbse.gov.in/results",
      "scraped_at": "2025-01-15T10:30:00Z"
    }
  ]
}
```

**Get Latest News:**
```json
{
  "news": [
    {
      "id": 456,
      "headline": "JEE Main 2025 Registration Begins",
      "article_link": "https://jeemain.nta.ac.in",
      "article_date": "2025-01-10",
      "scraped_at": "2025-01-10T08:00:00Z"
    }
  ]
}
```

---

## 🖥️ Installation & Setup

### Prerequisites

- Python 3.10 or higher
- Chrome/Chromium browser (for Selenium)
- ChromeDriver (or use webdriver-manager)
- Supabase account and project
- Zoho Mail account (for email notifications)
- Google Cloud Console project (for OAuth)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/pratham2025/GETNOTIFY.git
cd GETNOTIFY
```

### 2️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `selenium` - Web scraping
- `undetected_chromedriver` - Anti-detection browser automation
- `beautifulsoup4` - HTML parsing
- `supabase` - Supabase Python client
- `yagmail` - Email service (Zoho SMTP)
- `requests` - HTTP requests
- `python-dotenv` - Environment variable management

### 3️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-service-role-key

# Email Configuration (Zoho SMTP)
SMTP_EMAIL=alerts@getnotify.in
SMTP_PASSWORD=your-zoho-app-password
SMTP_HOST=smtppro.zoho.in
SMTP_PORT=587
```

### 4️⃣ Setup Supabase Database

#### Create Tables

1. **Announcements Table:**
```sql
CREATE TABLE announcements (
    id BIGSERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    text TEXT NOT NULL,
    link TEXT NOT NULL,
    scraped_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(source, text)
);

CREATE INDEX idx_announcements_source ON announcements(source);
CREATE INDEX idx_announcements_scraped_at ON announcements(scraped_at DESC);
```

2. **Subscriptions Table:**
```sql
CREATE TABLE subscriptions (
    id BIGSERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    source TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(email, source)
);

CREATE INDEX idx_subscriptions_email ON subscriptions(email);
CREATE INDEX idx_subscriptions_source ON subscriptions(source);
```

3. **Latest News Table:**
```sql
CREATE TABLE latest_news (
    id BIGSERIAL PRIMARY KEY,
    headline TEXT NOT NULL,
    article_link TEXT NOT NULL,
    article_date DATE,
    scraped_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_latest_news_scraped_at ON latest_news(scraped_at DESC);
```

#### Enable Row Level Security (RLS)

Configure RLS policies based on your security requirements. For public read access:

```sql
-- Allow public read access to announcements
ALTER TABLE announcements ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read access" ON announcements FOR SELECT USING (true);

-- Allow authenticated users to manage subscriptions
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can manage own subscriptions" ON subscriptions
    FOR ALL USING (auth.uid()::text = email);
```

### 5️⃣ Configure Frontend

Update `frontend/secrets.js` with your Supabase credentials:

```javascript
window.SUPABASE = {
  url: "https://your-project-id.supabase.co",
  anonKey: "your-supabase-anon-key"
};
```

**⚠️ Important:** Use the **anon key** (public key), never the service role key in frontend code.

### 6️⃣ Setup Google OAuth

1. **Supabase Dashboard:**
   - Go to Authentication → Providers
   - Enable Google provider
   - Enter Google OAuth Client ID and Secret

2. **Google Cloud Console:**
   - Create OAuth 2.0 credentials
   - Add authorized redirect URI: `https://your-project-id.supabase.co/auth/v1/callback`
   - Add authorized JavaScript origins (your frontend URLs)

See `frontend/OAUTH_SETUP.md` for detailed instructions.

### 7️⃣ Configure ChromeDriver

The worker uses a local ChromeDriver path. Update `worker.py` line 44 with your ChromeDriver path:

```python
service = ChromeService(r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe")
```

Or use `webdriver-manager` for automatic management (modify `setup_driver()` function).

### 8️⃣ Start the Services

#### Start FastAPI Backend

```bash
# Development (localhost only)
uvicorn scraper_api:app --reload --host 127.0.0.1 --port 8000

# Production (network access)
uvicorn scraper_api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

#### Start Background Worker

In a separate terminal:

```bash
python worker.py
```

The worker will:
- Load sources from `config.json`
- Scrape all sources in parallel (every hour by default)
- Save new announcements to Supabase
- Send email notifications to subscribers

**Configuration:**
- `SCRAPE_INTERVAL_SECONDS` - Time between scraping cycles (default: 3600 = 1 hour)
- `MAX_ANNOUNCEMENTS_PER_SOURCE` - Limit announcements per source (default: 60)

#### Launch Frontend

Simply open `frontend/home.html` or `frontend/index.html` in your web browser.

For development with live reload, use a local server:

```bash
# Using Python
cd frontend
python -m http.server 5500

# Using Node.js (http-server)
npx http-server -p 5500
```

Then visit `http://localhost:5500/home.html`

---

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t getnotify .
```

### Run with Docker Compose

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database (if configured)
- FastAPI backend
- Background worker

### Manual Docker Run

```bash
docker run -p 8000:8000 \
  -e SUPABASE_URL=your-url \
  -e SUPABASE_KEY=your-key \
  -e SMTP_EMAIL=your-email \
  -e SMTP_PASSWORD=your-password \
  getnotify
```

---

## 🔧 Configuration

### Source Configuration (`config.json`)

Add or modify sources in `config.json`:

```json
{
  "sources": [
    {
      "name": "CBSE",
      "url": "https://www.cbse.gov.in/cbsenew/cbse.html"
    },
    {
      "name": "JEE",
      "url": "https://jeemain.nta.nic.in/public-notices/"
    }
  ]
}
```

### Worker Configuration (`worker.py`)

```python
SCRAPE_INTERVAL_SECONDS = 3600  # 1 hour
MAX_ANNOUNCEMENTS_PER_SOURCE = 60
```

### API CORS Configuration (`scraper_api.py`)

Update `origins` list to include your frontend domains:

```python
origins = [
    "http://localhost:5500",
    "https://yourdomain.com",
    "*"  # For development only
]
```

---

## 📧 Email Notification System

### How It Works

1. **User Subscribes:** User clicks "Subscribe" button on a source card (requires login)
2. **Subscription Stored:** Email and source saved in Supabase `subscriptions` table
3. **Scraper Finds New Announcements:** Worker detects new announcements
4. **Emails Sent:** All subscribers for that source receive HTML email with new announcements

### Email Features

- **HTML Formatted:** Beautiful email templates with styling
- **Up to 10 Announcements:** Shows most recent announcements per email
- **Source Branding:** Includes source name and logo
- **Unsubscribe Info:** Instructions to manage subscriptions

### Email Service Configuration

The system uses **Zoho SMTP** via `yagmail`. To use a different provider:

1. Update `send_email.py` with your SMTP settings
2. Modify SMTP configuration in `.env` file

---

## 🧪 Testing

### Test Email Service

```bash
python test_mail.py
```

### Test Scraper Manually

```bash
# Test a specific scraper
python -c "from scrapers.cbse_scraper import scrape; from selenium import webdriver; driver = webdriver.Chrome(); print(scrape(driver))"
```

### Test API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Get sources
curl http://localhost:8000/sources

# Get announcements
curl http://localhost:8000/announcements/CBSE

# Subscribe
curl -X POST http://localhost:8000/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "source": "CBSE"}'
```

---

## 🛠️ Development

### Adding a New Scraper

1. **Create scraper module** in `scrapers/` directory:

```python
# scrapers/newsource_scraper.py
import logging
from bs4 import BeautifulSoup

def scrape(driver):
    """Scrape announcements from NewSource website."""
    logging.info("Scraping NewSource website")
    results = []
    
    try:
        driver.get("https://newsource.gov.in")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Your scraping logic here
        for item in soup.select('.announcement-item'):
            text = item.text.strip()
            link = item.find('a')['href']
            results.append({"text": text, "link": link})
        
        logging.info(f"Found {len(results)} announcements for NewSource")
    except Exception as e:
        logging.error(f"Error scraping NewSource: {e}")
    
    return results
```

2. **Add source to `config.json`:**

```json
{
  "name": "NewSource",
  "url": "https://newsource.gov.in"
}
```

3. **Add to SourceEnum in `scraper_api.py`:**

```python
class SourceEnum(str, Enum):
    # ... existing sources
    NEWSOURCE = "NewSource"
```

4. **Add logo** to `frontend/src/logos/` (optional)
5. **Add metadata** to `frontend/app.js` SOURCE_INFO (optional)

### Scraper Types

Scrapers can use either:
- **Selenium** (for JavaScript-heavy sites): Implement `scrape(driver)` function
- **Requests** (for static sites): Implement `scrape_requests()` function

The API automatically detects which method to use.

---

## 📊 Database Schema

### Announcements Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGSERIAL | Primary key |
| `source` | TEXT | Source name (e.g., "CBSE") |
| `text` | TEXT | Announcement text/headline |
| `link` | TEXT | URL to full announcement |
| `scraped_at` | TIMESTAMPTZ | When announcement was scraped |

**Indexes:**
- `idx_announcements_source` on `source`
- `idx_announcements_scraped_at` on `scraped_at DESC`

### Subscriptions Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGSERIAL | Primary key |
| `email` | TEXT | Subscriber email address |
| `source` | TEXT | Source to subscribe to |
| `created_at` | TIMESTAMPTZ | Subscription creation time |

**Constraints:**
- UNIQUE(`email`, `source`)

### Latest News Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGSERIAL | Primary key |
| `headline` | TEXT | News headline |
| `article_link` | TEXT | URL to full article |
| `article_date` | DATE | Publication date |
| `scraped_at` | TIMESTAMPTZ | When news was scraped |

---

## 🚀 Production Deployment

### Recommended Setup

1. **Use Process Manager:**
   - `systemd` (Linux)
   - `PM2` (Node.js process manager for Python)
   - `supervisord`

2. **Reverse Proxy:**
   - Nginx for frontend static files
   - Nginx as reverse proxy for FastAPI

3. **Database:**
   - Use Supabase production instance
   - Configure connection pooling
   - Enable backups

4. **Monitoring:**
   - Set up logging aggregation
   - Monitor API health endpoints
   - Track scraper success/failure rates

5. **Security:**
   - Use environment variables (never commit secrets)
   - Enable HTTPS
   - Configure CORS properly
   - Set up rate limiting
   - Use Supabase RLS policies

### Example Nginx Configuration

```nginx
server {
    listen 80;
    server_name getnotify.in;

    # Frontend static files
    location / {
        root /var/www/getnotify/frontend;
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🐛 Troubleshooting

### Common Issues

**1. Scraper fails with "ChromeDriver not found"**
- Install ChromeDriver or update path in `worker.py`
- Use `webdriver-manager` for automatic management

**2. "Supabase connection failed"**
- Verify `.env` file has correct `SUPABASE_URL` and `SUPABASE_KEY`
- Check Supabase project is active
- Verify network connectivity

**3. "Email not sending"**
- Verify Zoho SMTP credentials in `.env`
- Check Zoho account allows SMTP access
- Verify sender email is verified in Zoho

**4. "OAuth login not working"**
- Check Google Cloud Console redirect URIs
- Verify Supabase OAuth configuration
- See `frontend/OAUTH_SETUP.md` for detailed guide

**5. "No announcements showing"**
- Check if worker is running
- Verify scrapers are working (check logs)
- Check Supabase database has data
- Verify API endpoints are accessible

**6. "CORS errors in browser"**
- Add your frontend URL to `origins` in `scraper_api.py`
- Check browser console for specific error

---

## 📚 Additional Documentation

- **Subscription Setup:** See `SUBSCRIPTION_SETUP.md`
- **OAuth Setup:** See `frontend/OAUTH_SETUP.md`
- **Database Schema:** See `create_subscriptions_table.sql`

---

## 🔮 Future Enhancements

- 🤖 **AI Summarization** - Automatic summarization of long announcements (partially implemented)
- 📅 **Personalized Dashboard** - Custom dashboard for followed sources
- 📤 **Push Notifications** - Browser push notifications for new announcements
- 🌗 **Dark Mode** - Theme toggle with persistent preference
- 📊 **Analytics Dashboard** - Track top sources, most active boards, user engagement
- 🔍 **Advanced Search** - Full-text search across all announcements
- 📱 **Mobile App** - React Native mobile application
- 🌐 **Multi-language Support** - Support for regional languages
- 📈 **Trending Topics** - Identify trending exam topics and keywords
- 🔔 **Custom Notification Rules** - User-defined filters for notifications

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Adding New Scrapers

See the "Adding a New Scraper" section above. Make sure to:
- Test the scraper thoroughly
- Handle errors gracefully
- Add appropriate logging
- Update documentation

---

## 📜 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.

---

## 🧑‍💻 Author

**Developed by:** [Pratham Patil (Bosco)](https://github.com/pratham2025)  
**Role:** Full Stack Developer & Data Engineer  
**Project:** Educational Notification & Scraping System  
**Tech Stack:** FastAPI · Supabase · Selenium · HTML/CSS/JS · Docker · PostgreSQL · Zoho SMTP

---

## 🙏 Acknowledgments

- **Supabase** - For the amazing backend-as-a-service platform
- **FastAPI** - For the high-performance web framework
- **Selenium** - For web automation capabilities
- **Educational Boards** - For providing public announcement data

---

### ⭐ Star this repo if you like the project!

> **"Stay informed, stay ahead — with GETNOTIFY!"**

---

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

---

**Last Updated:** January 2025  
**Version:** 3.0  
**Status:** Production Ready 🚀
