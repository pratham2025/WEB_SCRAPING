# 🔄 Worker Deployment Guide

## 🎯 What is the Worker?

The **worker** (`worker.py`) is a background process that:
- ✅ Scrapes all exam boards **every hour** (configurable)
- ✅ Saves new announcements to Supabase
- ✅ Sends email notifications to subscribers
- ✅ Runs **24/7** continuously

**Current Setup:**
- Scrapes every **3600 seconds** (1 hour)
- Runs in parallel (up to 10 sources at once)
- Needs Chrome/Selenium to work

---

## 🚀 Where Should the Worker Run?

You have **3 main options**:

### **Option 1: Render Background Worker** ⭐ **RECOMMENDED**

**Best for:** Simple, managed solution

**Pros:**
- ✅ Easy setup
- ✅ Managed by Render
- ✅ Automatic restarts
- ✅ Built-in logging
- ✅ Free tier available (with limits)

**Cons:**
- ⚠️ Free tier has limitations
- ⚠️ Paid tier: $7/month

**Setup:**
1. Go to Render Dashboard
2. Click **"New +"** → **"Background Worker"**
3. Connect your GitHub repo
4. Configure:
   - **Name**: `getnotify-worker`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python worker.py`
5. Add environment variables:
   ```
   SUPABASE_URL=your-url
   SUPABASE_KEY=your-key
   SENDGRID_API_KEY=your-key (optional)
   ```
6. Deploy!

---

### **Option 2: GitHub Actions (Free)** ⭐ **BEST VALUE**

**Best for:** Free, reliable scheduling

**Pros:**
- ✅ **100% FREE**
- ✅ Reliable (GitHub infrastructure)
- ✅ Easy to schedule
- ✅ Good for hourly/daily scraping

**Cons:**
- ⚠️ Requires Chrome setup in GitHub Actions
- ⚠️ Slightly more complex setup

**Setup:**
1. Create `.github/workflows/scraper.yml` in your repo
2. GitHub Actions will run it on schedule
3. See example below

---

### **Option 3: Separate Render Service**

**Best for:** More control, same platform

**Pros:**
- ✅ Same platform as your API
- ✅ Easy to manage
- ✅ Good logging

**Cons:**
- ⚠️ Costs $7/month (paid tier)
- ⚠️ Free tier spins down (not good for workers)

**Setup:**
1. Create new **Web Service** on Render
2. Use same config as API
3. Set start command to: `python worker.py`
4. Keep it running 24/7

---

## 📋 Recommended: GitHub Actions (Free)

Since you want to keep costs low, **GitHub Actions is the best option**. Here's how:

### Step 1: Create GitHub Actions Workflow

Create file: `.github/workflows/scraper.yml`

```yaml
name: Scrape Exam Boards

on:
  schedule:
    # Run every 6 hours (adjust as needed)
    - cron: '0 */6 * * *'
  workflow_dispatch:  # Allow manual trigger

jobs:
  scrape:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install Chrome
      run: |
        sudo apt-get update
        sudo apt-get install -y google-chrome-stable
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run scraper
      env:
        SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
        SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
        SENDGRID_API_KEY: ${{ secrets.SENDGRID_API_KEY }}
      run: |
        python -c "
        import time
        import logging
        import json
        import importlib
        import concurrent.futures
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from supabase import create_client
        import os
        
        # Load config
        with open('config.json', 'r') as f:
            sources = json.load(f).get('sources', [])
        
        # Setup Supabase
        supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
        
        # Setup Chrome
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        def scrape_source(source_config):
            driver = None
            try:
                driver = webdriver.Chrome(options=options)
                module_name = f'scrapers.{source_config[\"name\"].lower()}_scraper'
                scraper = importlib.import_module(module_name)
                
                if source_config['name'] not in ['CBSE', 'JEE']:
                    driver.get(source_config['url'])
                
                data = scraper.scrape(driver)
                
                # Save to Supabase
                for item in data or []:
                    existing = supabase.table('announcements').select('id').eq('source', source_config['name']).eq('text', item.get('text', '')).limit(1).execute()
                    if not existing.data:
                        supabase.table('announcements').insert({
                            'source': source_config['name'],
                            'text': item.get('text', ''),
                            'link': item.get('link', ''),
                            'scraped_at': time.strftime('%Y-%m-%dT%H:%M:%SZ')
                        }).execute()
                
                return {'source': source_config['name'], 'status': 'Success'}
            except Exception as e:
                return {'source': source_config['name'], 'status': f'Failed: {e}'}
            finally:
                if driver:
                    driver.quit()
        
        # Run scrapers in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(scrape_source, sources))
        
        print('Scraping complete:', results)
        "
```

### Step 2: Add GitHub Secrets

1. Go to your GitHub repo
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Add these secrets:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `SENDGRID_API_KEY` (optional)

### Step 3: Test

1. Push the workflow file to GitHub
2. Go to **Actions** tab in your repo
3. You can manually trigger it to test
4. It will run automatically on schedule

---

## 🔧 Alternative: Use Render API Endpoint

Instead of running worker separately, you can trigger scraping via your API:

### Option A: Manual Trigger (via API)

Your API already has endpoints:
- `POST /scrape/{source}` - Scrape one source
- `POST /scrape_all` - Scrape all sources

You can call these from:
- **GitHub Actions** (free cron)
- **Cron-job.org** (free external service)
- **Render Cron Jobs** (paid)

### Example: GitHub Actions calling your API

```yaml
name: Trigger Scraping

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
    - name: Trigger Scrape All
      run: |
        curl -X POST https://api.getnotify.in/scrape_all
```

**Pros:**
- ✅ Uses your existing API
- ✅ No Chrome setup needed
- ✅ Very simple

**Cons:**
- ⚠️ Depends on your API being up
- ⚠️ Free tier API might spin down

---

## 💰 Cost Comparison

| Option | Cost | Reliability | Setup Difficulty |
|--------|------|-------------|------------------|
| **GitHub Actions** | **FREE** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ Medium |
| **Render Background Worker** | $7/month | ⭐⭐⭐⭐ | ⭐⭐ Easy |
| **Render Service** | $7/month | ⭐⭐⭐⭐ | ⭐⭐ Easy |
| **API Endpoint + Cron** | FREE | ⭐⭐⭐ | ⭐ Very Easy |

---

## 🎯 My Recommendation

**For your situation:**

1. **Start with**: GitHub Actions calling your API (`/scrape_all`)
   - ✅ Free
   - ✅ Simple
   - ✅ Reliable
   - ✅ No Chrome setup needed

2. **If that doesn't work**: Use GitHub Actions with full worker
   - ✅ Free
   - ✅ More control
   - ⚠️ Requires Chrome setup

3. **If you need 24/7**: Render Background Worker
   - ✅ Always running
   - ⚠️ Costs $7/month

---

## 📝 Quick Setup (Recommended)

### Use API Endpoint + GitHub Actions

1. **Create**: `.github/workflows/scrape.yml`

```yaml
name: Scrape Exam Boards

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
    - name: Trigger Scrape
      run: |
        curl -X POST https://api.getnotify.in/scrape_all
```

2. **Push to GitHub**
3. **Done!** It will run automatically every 6 hours

---

## ✅ Checklist

- [ ] Choose deployment option
- [ ] Set up worker/cron
- [ ] Test scraping works
- [ ] Verify announcements appear in Supabase
- [ ] Check email notifications (if enabled)
- [ ] Monitor logs

---

## 🐛 Troubleshooting

### Worker not running:
- Check logs in Render/GitHub Actions
- Verify environment variables are set
- Check Chrome/Selenium setup

### Scraping fails:
- Check if websites are accessible
- Verify scraper modules are correct
- Check Supabase connection

### No new announcements:
- Check if websites changed structure
- Verify scrapers are working
- Check Supabase for errors

---

## 🎉 Summary

**Best Option for You:**
- **GitHub Actions** calling your API endpoint (`/scrape_all`)
- **Free**, **Simple**, **Reliable**
- Runs every 6 hours (adjustable)

Your worker will scrape exam boards automatically and keep your database updated! 🚀
