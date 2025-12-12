# 🚀 Deployment Guide - GETNOTIFY

This guide will help you deploy your GETNOTIFY web scraping application to the internet. We'll cover multiple deployment options.

## 📋 Prerequisites

Before deploying, make sure you have:
- ✅ A Supabase account and project (already configured)
- ✅ All environment variables ready
- ✅ A GitHub account (for easy deployment)
- ✅ Your code pushed to a GitHub repository

---

## 🎯 Option 1: Render.com (Recommended - Easiest)

Render.com is great for Python/FastAPI apps and offers free tier.

### Step 1: Prepare Your Repository

1. Push your code to GitHub:
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

### Step 2: Deploy Backend API

1. Go to [Render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `getnotify-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn scraper_api:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (or choose paid for better performance)

5. **Add Environment Variables** (in Render dashboard):
   ```
   SUPABASE_URL=https://hfsazlirxtjbarftyoqh.supabase.co
   SUPABASE_KEY=your-service-role-key-here
   SENDGRID_API_KEY=your-sendgrid-key (optional)
   ```

6. Click **"Create Web Service"**
7. Wait for deployment (5-10 minutes)
8. Your API will be available at: `https://getnotify-api.onrender.com`

### Step 3: Deploy Frontend

**Option A: Render Static Site**
1. In Render, click **"New +"** → **"Static Site"**
2. Connect your GitHub repo
3. Configure:
   - **Name**: `getnotify-frontend`
   - **Build Command**: (leave empty)
   - **Publish Directory**: `frontend`
4. Add a **Rewrite Rule**: `/*` → `/index.html`
5. Deploy!

**Option B: Vercel (Recommended for Frontend)**
- See Option 2 below for Vercel deployment

### Step 4: Update Frontend API URL

After backend is deployed, update your frontend to use the production API:

1. In your `frontend/index.html` (and other HTML files), add this in the `<head>`:
   ```html
   <meta name="api-base-url" content="https://getnotify-api.onrender.com">
   ```

2. Or update `frontend/app.js` to use your Render API URL directly.

---

## 🎯 Option 2: Vercel (Frontend) + Railway (Backend)

### Deploy Backend to Railway

1. Go to [Railway.app](https://railway.app) and sign up
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway will auto-detect the Dockerfile
5. Add environment variables in Railway dashboard:
   ```
   SUPABASE_URL=https://hfsazlirxtjbarftyoqh.supabase.co
   SUPABASE_KEY=your-service-role-key
   SENDGRID_API_KEY=your-sendgrid-key
   ```
6. Railway will automatically deploy and give you a URL like: `https://your-app.railway.app`

### Deploy Frontend to Vercel

1. Go to [Vercel.com](https://vercel.com) and sign up
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `frontend`
   - **Build Command**: (leave empty)
   - **Output Directory**: `.` (current directory)
5. Add Environment Variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-app.railway.app
   ```
6. Deploy!

---

## 🎯 Option 3: Docker + Any Cloud Provider

### Build Docker Image

```bash
docker build -t getnotify-api .
```

### Run Locally (Test)

```bash
docker run -p 8000:8000 \
  -e SUPABASE_URL=your-url \
  -e SUPABASE_KEY=your-key \
  getnotify-api
```

### Deploy to Cloud Run (Google Cloud)

1. Install Google Cloud SDK
2. Build and push:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT/getnotify-api
   gcloud run deploy getnotify-api \
     --image gcr.io/YOUR_PROJECT/getnotify-api \
     --platform managed \
     --region us-central1 \
     --set-env-vars SUPABASE_URL=your-url,SUPABASE_KEY=your-key
   ```

### Deploy to AWS Elastic Beanstalk

1. Install EB CLI: `pip install awsebcli`
2. Initialize: `eb init`
3. Create environment: `eb create`
4. Set environment variables in AWS Console

---

## 🔧 Post-Deployment Configuration

### 1. Update Supabase Redirect URLs

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Navigate to **Authentication** → **URL Configuration**
3. Add your production frontend URL to **Site URL**
4. Add redirect URLs:
   - `https://your-frontend-domain.com`
   - `https://your-frontend-domain.com/auth/callback`

### 2. Update Google OAuth Settings

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to **APIs & Services** → **Credentials**
3. Edit your OAuth 2.0 Client
4. Add authorized redirect URIs:
   - `https://hfsazlirxtjbarftyoqh.supabase.co/auth/v1/callback`
   - `https://your-frontend-domain.com`

### 3. Update Frontend API Configuration

Update `frontend/app.js` and `frontend/home.js` to use your production API URL, or add a meta tag in your HTML:

```html
<meta name="api-base-url" content="https://your-api-domain.com">
```

### 4. Configure CORS (if needed)

If your frontend and backend are on different domains, update CORS in `scraper_api.py`:

```python
origins = [
    "https://your-frontend-domain.com",
    "https://www.your-frontend-domain.com",
]
```

---

## 🧪 Testing Your Deployment

1. **Test API Health**:
   ```bash
   curl https://your-api-domain.com/health
   ```

2. **Test API Endpoints**:
   ```bash
   curl https://your-api-domain.com/sources
   curl https://your-api-domain.com/announcements/CBSE
   ```

3. **Test Frontend**:
   - Visit your frontend URL
   - Check browser console for errors
   - Test login functionality
   - Test fetching announcements

---

## 📊 Monitoring & Maintenance

### Set Up Logging

- Render: View logs in dashboard
- Railway: View logs in dashboard
- Vercel: View logs in dashboard

### Set Up Scheduled Scraping

You can use:
- **Render Cron Jobs** (paid plans)
- **GitHub Actions** (free)
- **Cron-job.org** (free external service)

Example GitHub Actions workflow (`.github/workflows/scrape.yml`):

```yaml
name: Daily Scrape
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Trigger Scrape
        run: |
          curl -X POST https://your-api-domain.com/scrape_all
```

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: API returns 500 errors
- Check environment variables are set correctly
- Check Supabase connection
- View logs in deployment platform

**Problem**: Chrome/Selenium errors
- Make sure Dockerfile includes Chrome installation
- Check if platform supports headless Chrome

### Frontend Issues

**Problem**: CORS errors
- Update CORS origins in `scraper_api.py`
- Make sure API URL is correct

**Problem**: API calls failing
- Check API URL in browser console
- Verify API is accessible
- Check network tab for errors

### Authentication Issues

**Problem**: Google OAuth not working
- Verify redirect URLs in Supabase and Google Console
- Check Site URL in Supabase dashboard
- Ensure frontend URL matches configured URLs

---

## 💰 Cost Estimates

### Free Tier Options:
- **Render**: Free tier (spins down after 15 min inactivity)
- **Railway**: $5 free credit/month
- **Vercel**: Free tier for static sites
- **Supabase**: Free tier (500MB database)

### Paid Options (if you need 24/7 uptime):
- **Render**: $7/month per service
- **Railway**: Pay-as-you-go (~$5-20/month)
- **Vercel Pro**: $20/month

---

## ✅ Quick Checklist

- [ ] Code pushed to GitHub
- [ ] Environment variables configured
- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] Supabase redirect URLs updated
- [ ] Google OAuth redirect URLs updated
- [ ] Frontend API URL configured
- [ ] CORS configured (if needed)
- [ ] Health check endpoint working
- [ ] Tested login functionality
- [ ] Tested announcement fetching

---

## 🎉 You're Done!

Your application should now be live on the internet! Share your URL and start getting users.

**Need Help?**
- Check the logs in your deployment platform
- Review error messages in browser console
- Verify all environment variables are set
- Test API endpoints directly with curl/Postman
