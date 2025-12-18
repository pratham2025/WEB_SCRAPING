# 📢 GETNOTIFY — Real-time Educational Notifications Platform

🚀 **Instant Exam Alerts, Smart Scraping, and Beautiful UI for Students Across India**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)  
![Supabase](https://img.shields.io/badge/Supabase-Cloud%20Database-3ECF8E)  
![HTML5](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-blue)  
![Python](https://img.shields.io/badge/Python-3.10+-yellow)  
![Docker](https://img.shields.io/badge/Docker-Supported-2496ED)  
![Selenium](https://img.shields.io/badge/Selenium-Web%20Scraping-43B02A)  
![Deployed](https://img.shields.io/badge/Status-Live%20Production-success)

---

## 🌐 Live Production URLs

- **🌍 Website**: [https://getnotify.in](https://getnotify.in)
- **🔌 API**: [https://api.getnotify.in](https://api.getnotify.in)
- **📊 Analytics**: Google Analytics integrated
- **☁️ Database**: Supabase Cloud PostgreSQL

---

## 🔎 Overview

**GETNOTIFY** is a comprehensive, **production-ready** platform that delivers **real-time educational notifications** from official sources across India. The system automatically scrapes announcements from **15+ educational boards and organizations** including NTA, CBSE, NEET, JEE, UPSC, ISRO, KSEAB, KEA, MAHACET, MPSC, RRB boards, GATE, and Indian Express.

### Production Stack
- **Frontend**: Deployed on **Vercel** (https://getnotify.in)
- **Backend API**: Deployed on **Render** (https://api.getnotify.in)
- **Database & Auth**: **Supabase** (Cloud PostgreSQL + Authentication)
- **Worker**: **GitHub Actions** (Automated scraping via cron)
- **Analytics**: **Google Analytics** (Page views & user tracking)
- **Email**: **SendGrid** (Email notifications to subscribers)

---

## 🧠 Core Features

### Web Scraping & Data Collection
- ⚡ **Real-time Web Scraping** using Selenium and undetected_chromedriver
- 🔄 **Parallel Processing** - scrapes multiple sources simultaneously (up to 10 workers)
- 🛡️ **Anti-Detection** - uses undetected_chromedriver to avoid bot detection
- 🔍 **Duplicate Detection** - prevents storing duplicate announcements
- ⏰ **Automated Scheduling** - GitHub Actions triggers scraping every 6 hours
- 📊 **15+ Source Support** - extensible scraper architecture

### User Features
- 🔔 **Email Subscriptions** - users can subscribe to specific sources for email notifications
- 🔐 **Account Options**  
  - **Google OAuth Login** via Supabase Auth (recommended)  
  - **Passwordless Manual Login** using just name + email (no password / verification – for faster onboarding)
- 📱 **Responsive Design** - optimized for desktop, tablet, and mobile devices (including mobile-friendly login modal)
- 🎨 **Beautiful UI** - modern glass-inspired design with animations
- 📰 **Latest News Board** - pinned paper-style cards with NEW badges
- 🔍 **Source Filtering** - browse announcements by educational board
- 📄 **Pagination** - efficient browsing of large announcement lists
- 📊 **Analytics** - Google Analytics tracking for page views

### Technical Features
- 🧩 **Modular Architecture** - separate scraper modules for each source
- 🗄️ **Supabase Integration** - cloud database with real-time capabilities
- 📧 **Email Notifications** - SendGrid integration for sending HTML emails
- 🚀 **FastAPI REST API** - high-performance async endpoints
- 🐳 **Docker Support** - containerized deployment ready
- 📝 **Comprehensive Logging** - detailed logs for debugging and monitoring
- 🌐 **Custom Domain** - Professional domain (getnotify.in) with SSL

---

## 🏗️ Production Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GETNOTIFY Production                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Users → https://getnotify.in (Vercel Frontend)            │
│              │                                               │
│              │ API Calls                                     │
│              ▼                                               │
│  https://api.getnotify.in (Render Backend)                  │
│              │                                               │
│              │ Database/Auth                                 │
│              ▼                                               │
│  Supabase Cloud (PostgreSQL + Auth)                         │
│              │                                               │
│              │ Email Service                                 │
│              ▼                                               │
│  SendGrid (Email Notifications)                             │
│                                                              │
│  ┌────────────────────────────────────────────┐            │
│  │ GitHub Actions (Automated Scraping)        │            │
│  │ Runs every 6 hours → Calls /scrape_all     │            │
│  └────────────────────────────────────────────┘            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
GETNOTIFY/
│
├── frontend/                          # Frontend application (Vercel)
│   ├── index.html                     # Marketing + hero page + latest news
│   ├── notifications.html             # Main notifications / exam source browser
│   ├── syllabus.html                  # Syllabus section (static page)
│   ├── answer_keys.html               # Answer keys section (static page)
│   ├── about-us.html                  # About the platform & vision
│   ├── our-story.html                 # Story of how a missed exam form inspired GETNOTIFY
│   ├── styles.css                     # Global styles (2567 lines)
│   ├── app.js                         # Source & announcement logic
│   ├── home.js                        # Homepage notice board logic
│   ├── common.js                      # Header/Footer injection
│   ├── auth.js                        # Auth: Supabase Google OAuth + manual (passwordless) login
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
├── scrapers/                          # Web scraper modules (15+ sources)
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
│   └── indianexpress_scraper.py        # Indian Express education news
│
├── scraper_api.py                     # FastAPI REST API server (Render)
├── worker.py                          # Background worker (legacy, use GitHub Actions)
├── notify_subscribers.py              # Email notification service
├── send_email.py                      # SendGrid email service
├── summarizer.py                      # AI text summarization (optional)
├── init_db.py                         # Database initialization (legacy)
├── web_scrape.py                      # Standalone scraper test script
├── test_mail.py                       # Email service test script
│
├── config.json                        # Source configuration (URLs & names)
├── requirements.txt                   # Python dependencies
├── docker-compose.yml                 # Docker Compose configuration
├── dockerfile                         # Docker image definition (production-ready)
├── .env                               # Environment variables (not in repo)
├── .gitignore                         # Git ignore rules
│
├── .github/
│   └── workflows/
│       └── scrape.yml                 # GitHub Actions automated scraping
│
├── Deployment Documentation/
│   ├── COMPLETE_DEPLOYMENT_GUIDE.md   # Full deployment guide
│   ├── DEPLOYMENT_GUIDE.md            # General deployment guide
│   ├── DEPLOYMENT_QUICK_START.md      # Quick start guide
│   ├── DEPLOYMENT_COMPARISON.md       # Platform comparison
│   ├── CUSTOM_DOMAIN_SETUP.md         # Custom domain setup
│   ├── DOMAIN_QUICK_SETUP.md          # Domain quick setup
│   ├── VERCEL_DEPLOYMENT_STEPS.md     # Vercel specific guide
│   ├── WORKER_DEPLOYMENT.md           # Worker deployment options
│   ├── FIX_LOGIN_ISSUE.md             # Login troubleshooting
│   └── FIX_GOOGLE_ANALYTICS.md        # Analytics troubleshooting
│
├── create_subscriptions_table.sql     # Supabase subscriptions table schema
├── SUBSCRIPTION_SETUP.md              # Subscription feature setup guide
├── Procfile                           # Render/Heroku process file
├── render.yaml                        # Render.com configuration
├── railway.json                       # Railway.app configuration
├── vercel.json                        # Vercel configuration
├── prepare_deployment.sh              # Deployment preparation script
├── prepare_deployment.bat             # Windows deployment script
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

| Method | Endpoint | Description | Example |
|--------|----------|-------------|---------|
| `GET` | `/` | API health check | `https://api.getnotify.in/` |
| `GET` | `/sources` | List all supported educational sources | `https://api.getnotify.in/sources` |
| `GET` | `/announcements/{source}` | Get announcements for a specific source | `https://api.getnotify.in/announcements/CBSE` |
| `GET` | `/latest-news` | Get latest educational news | `https://api.getnotify.in/latest-news` |
| `GET` | `/health` | Check API and database connection status | `https://api.getnotify.in/health` |

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
  "sources": ["CBSE", "JEE", "NEET", "NTA", "UPSC", "GATE", "ISRO", "KSEAB", "KEA", "MAHACET", "MPSC", "RRBKolkata", "RRBMumbai", "RRBAhmedabad", "IndianExpress"]
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

---

## 🚀 Quick Start (Production)

### For Users
Visit **[https://getnotify.in](https://getnotify.in)** to start using the platform!

### For Developers

#### 1️⃣ Clone Repository
```bash
git clone https://github.com/pratham2025/WEB_SCRAPING.git
cd WEB_SCRAPING
```

#### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3️⃣ Configure Environment
Create `.env` file:
```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-service-role-key

# SendGrid (for email notifications)
SENDGRID_API_KEY=your-sendgrid-api-key
```

#### 4️⃣ Run Locally
```bash
# Start API (from project root)
uvicorn scraper_api:app --reload --host 0.0.0.0 --port 8000

# Frontend (in another terminal, from project root)
cd frontend
python -m http.server 5500
```

Then open in the browser:
- `http://localhost:5500/index.html`  → public landing page + latest news  
- `http://localhost:5500/notifications.html`  → full notifications & sources UI

---

## 🖥️ Installation & Setup (Detailed)

### Prerequisites

- Python 3.10 or higher
- Chrome/Chromium browser (for Selenium)
- Supabase account and project
- SendGrid account (for email notifications)
- Google Cloud Console project (for OAuth)
- Domain name (optional, for custom domain)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/pratham2025/WEB_SCRAPING.git
cd WEB_SCRAPING
```

### 2️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- `fastapi` - Web framework
- `uvicorn[standard]` - ASGI server
- `selenium` - Web scraping
- `undetected-chromedriver` - Anti-detection browser automation
- `beautifulsoup4` - HTML parsing
- `supabase` - Supabase Python client
- `sendgrid` - Email service
- `requests` - HTTP requests
- `python-dotenv` - Environment variable management

### 3️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-service-role-key

# SendGrid Configuration (for email notifications)
SENDGRID_API_KEY=your-sendgrid-api-key
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

Configure RLS policies based on your security requirements:

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
   - Add your frontend URLs to authorized JavaScript origins

See `frontend/OAUTH_SETUP.md` for detailed instructions.

### 7️⃣ Start the Services

#### Start FastAPI Backend

```bash
# Development (localhost only)
uvicorn scraper_api:app --reload --host 127.0.0.1 --port 8000

# Production (network access)
uvicorn scraper_api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

#### Launch Frontend

Simply open `frontend/home.html` or `frontend/index.html` in your web browser.

For development with live reload:
```bash
cd frontend
python -m http.server 5500
```

Then visit `http://localhost:5500/home.html`

---

## 🚀 Production Deployment

### Current Production Setup

**Frontend (Vercel):**
- URL: `https://getnotify.in`
- Auto-deploys from GitHub
- Custom domain configured
- Google Analytics integrated

**Backend (Render):**
- URL: `https://api.getnotify.in`
- Python 3.10 environment
- Environment variables configured
- Free tier (spins down after inactivity)

**Database (Supabase):**
- Cloud PostgreSQL
- Authentication enabled
- Row Level Security configured

**Worker (GitHub Actions):**
- Automated scraping every 6 hours
- Calls `/scrape_all` endpoint
- Free and reliable

### Deployment Guides

- **📖 Complete Guide**: See `COMPLETE_DEPLOYMENT_GUIDE.md`
- **⚡ Quick Start**: See `DEPLOYMENT_QUICK_START.md`
- **🌐 Custom Domain**: See `CUSTOM_DOMAIN_SETUP.md`
- **🔄 Worker Setup**: See `WORKER_DEPLOYMENT.md`
- **🔐 Login Issues**: See `FIX_LOGIN_ISSUE.md`
- **📊 Analytics Setup**: See `FIX_GOOGLE_ANALYTICS.md`

### Quick Deployment Steps

1. **Deploy Backend to Render:**
   - Connect GitHub repo
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn scraper_api:app --host 0.0.0.0 --port $PORT`
   - Add environment variables

2. **Deploy Frontend to Vercel:**
   - Connect GitHub repo
   - Set root directory: `frontend`
   - Deploy!

3. **Setup Custom Domain:**
   - Add domain in Vercel
   - Add subdomain in Render (`api.getnotify.in`)
   - Configure DNS records
   - Update Supabase redirect URLs

4. **Setup Automated Scraping:**
   - Push `.github/workflows/scrape.yml` to GitHub
   - GitHub Actions will run automatically

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

### Manual Docker Run

```bash
docker run -p 8000:8000 \
  -e SUPABASE_URL=your-url \
  -e SUPABASE_KEY=your-key \
  -e SENDGRID_API_KEY=your-key \
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

### API CORS Configuration (`scraper_api.py`)

Update `origins` list to include your frontend domains:

```python
origins = [
    "https://getnotify.in",
    "https://www.getnotify.in",
    "http://localhost:5500",
    "*"  # For development only
]
```

### Frontend API Configuration

The frontend automatically detects the API URL:
- Production: Uses `https://api.getnotify.in`
- Development: Uses `http://localhost:8000`

You can override with a meta tag:
```html
<meta name="api-base-url" content="https://api.getnotify.in">
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

### Email Service

The system uses **SendGrid** for email delivery. Configure in `.env`:
```env
SENDGRID_API_KEY=your-sendgrid-api-key
```

---

## 🔄 Automated Scraping (GitHub Actions)

The project uses **GitHub Actions** for automated scraping:

**Location:** `.github/workflows/scrape.yml`

**Schedule:** Runs every 6 hours (configurable)

**How it works:**
1. GitHub Actions triggers on schedule
2. Calls `POST https://api.getnotify.in/scrape_all`
3. Render API scrapes all sources
4. Saves to Supabase
5. Sends email notifications

**To modify schedule:**
Edit `.github/workflows/scrape.yml` and change the cron expression:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
```

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
curl https://api.getnotify.in/health

# Get sources
curl https://api.getnotify.in/sources

# Get announcements
curl https://api.getnotify.in/announcements/CBSE

# Subscribe
curl -X POST https://api.getnotify.in/subscribe \
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

## 🐛 Troubleshooting

### Common Issues

**1. Scraper fails with "ChromeDriver not found"**
- Install ChromeDriver or update path in `worker.py`
- Use `webdriver-manager` for automatic management
- In production (Render), Chrome is pre-installed in Docker

**2. "Supabase connection failed"**
- Verify `.env` file has correct `SUPABASE_URL` and `SUPABASE_KEY`
- Check Supabase project is active
- Verify network connectivity

**3. "Email not sending"**
- Verify SendGrid API key in `.env`
- Check SendGrid account is active
- Verify sender email is verified in SendGrid

**4. "OAuth login not working"**
- Check Google Cloud Console redirect URIs
- Verify Supabase OAuth configuration
- See `FIX_LOGIN_ISSUE.md` for detailed guide

**5. "No announcements showing"**
- Check if GitHub Actions workflow is running
- Verify scrapers are working (check Render logs)
- Check Supabase database has data
- Verify API endpoints are accessible

**6. "CORS errors in browser"**
- Add your frontend URL to `origins` in `scraper_api.py`
- Check browser console for specific error

**7. "Google Analytics not detected"**
- Verify code is deployed to Vercel
- Check page source for Google Analytics code
- Wait 15-30 minutes for Google to detect
- See `FIX_GOOGLE_ANALYTICS.md` for detailed guide

---

## 📚 Additional Documentation

### Deployment Guides
- **Complete Deployment**: `COMPLETE_DEPLOYMENT_GUIDE.md`
- **Quick Start**: `DEPLOYMENT_QUICK_START.md`
- **Platform Comparison**: `DEPLOYMENT_COMPARISON.md`
- **Custom Domain**: `CUSTOM_DOMAIN_SETUP.md`
- **Vercel Steps**: `VERCEL_DEPLOYMENT_STEPS.md`
- **Worker Deployment**: `WORKER_DEPLOYMENT.md`

### Setup Guides
- **Subscription Setup**: `SUBSCRIPTION_SETUP.md`
- **OAuth Setup**: `frontend/OAUTH_SETUP.md`
- **Database Schema**: `create_subscriptions_table.sql`

### Troubleshooting
- **Login Issues**: `FIX_LOGIN_ISSUE.md`
- **Analytics Issues**: `FIX_GOOGLE_ANALYTICS.md`
- **Mobile Access**: `frontend/MOBILE_ACCESS_FIX.md`

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
**Tech Stack:** FastAPI · Supabase · Selenium · HTML/CSS/JS · Docker · PostgreSQL · SendGrid · Vercel · Render

---

## 🙏 Acknowledgments

- **Supabase** - For the amazing backend-as-a-service platform
- **FastAPI** - For the high-performance web framework
- **Selenium** - For web automation capabilities
- **Vercel** - For excellent frontend hosting
- **Render** - For reliable backend hosting
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
- Visit the live site: [https://getnotify.in](https://getnotify.in)

---

**Last Updated:** January 2025  
**Version:** 3.0  
**Status:** ✅ Production Ready & Live 🚀  
**Live URL:** [https://getnotify.in](https://getnotify.in)
