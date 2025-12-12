# 🎯 Complete Deployment Guide: Render + Vercel + Supabase

## ✅ Current Status

- ✅ **Backend (API)**: Deployed to Render at `https://web-scraping-7dzj.onrender.com`
- ✅ **Frontend**: Ready to deploy to Vercel
- ✅ **Database & Auth**: Supabase (already configured)
- ✅ **API URL**: Updated in frontend files

---

## 🚀 Step-by-Step Deployment

### **STEP 1: Verify Backend is Working**

Test your Render backend:

```bash
# Test health endpoint
curl https://web-scraping-7dzj.onrender.com/health

# Test sources endpoint
curl https://web-scraping-7dzj.onrender.com/sources

# Test announcements
curl https://web-scraping-7dzj.onrender.com/announcements/CBSE
```

**Expected Response:**
- Health: `{"status": "healthy", "supabase_connected": true}`
- Sources: `{"sources": ["CBSE", "JEE", ...]}`
- Announcements: `{"source": "CBSE", "data": [...]}`

---

### **STEP 2: Push Updated Code to GitHub**

Your frontend files are now configured with the Render API URL. Push to GitHub:

```bash
# Navigate to your project
cd e:\STARTUP\WEB_SCRAPING

# Check what changed
git status

# Add all changes
git add .

# Commit
git commit -m "Configure frontend for Render backend deployment"

# Push to GitHub
git push origin master
```

**Verify on GitHub:**
- Go to your repository
- Check that `frontend/index.html` and `frontend/home.html` have the API URL meta tag

---

### **STEP 3: Deploy Frontend to Vercel**

#### 3.1 Sign Up / Login to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click **"Sign Up"** or **"Log In"**
3. Choose **"Continue with GitHub"**
4. Authorize Vercel to access your repositories

#### 3.2 Import Your Project
1. Click **"Add New..."** → **"Project"**
2. You'll see your GitHub repositories
3. Find **`WEB_SCRAPING`** (or `pratham2025/WEB_SCRAPING`)
4. Click **"Import"**

#### 3.3 Configure Project Settings

**⚠️ IMPORTANT SETTINGS:**

| Setting | Value | Why |
|---------|-------|-----|
| **Framework Preset** | `Other` | Your app is vanilla HTML/JS |
| **Root Directory** | `frontend` | ⚠️ **CRITICAL!** Your frontend files are in `/frontend` folder |
| **Build Command** | (leave empty) | No build step needed |
| **Output Directory** | `.` | Current directory |
| **Install Command** | (leave empty) | No dependencies to install |

**Visual Guide:**
```
Project Name: web-scraping (or your choice)
Framework Preset: Other
Root Directory: frontend  ← Click "Edit" and set this!
Build Command: (empty)
Output Directory: .
Install Command: (empty)
```

#### 3.4 Environment Variables (Optional)
You can skip this - the API URL is already in the HTML files.

If you want to use env vars instead:
- Key: `NEXT_PUBLIC_API_URL`
- Value: `https://web-scraping-7dzj.onrender.com`

#### 3.5 Deploy!
1. Click **"Deploy"** button
2. Wait 1-2 minutes
3. Watch the build logs
4. **Success!** You'll get a URL like: `https://web-scraping-xxxxx.vercel.app`

#### 3.6 Test Your Frontend
1. Visit your Vercel URL
2. Open browser console (F12)
3. Check for any errors
4. Try navigating the site
5. Test the API connection (should work automatically)

---

### **STEP 4: Update Supabase Configuration**

Your frontend will need to authenticate with Supabase. Update redirect URLs:

#### 4.1 Update Supabase Site URL
1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to **Authentication** → **URL Configuration**
4. Update **Site URL**:
   ```
   https://your-vercel-url.vercel.app
   ```
   (Replace with your actual Vercel URL)

#### 4.2 Add Redirect URLs
In the same page, add these **Redirect URLs**:
```
https://your-vercel-url.vercel.app
https://your-vercel-url.vercel.app/auth/callback
https://web-scraping-7dzj.onrender.com
```

#### 4.3 Update Google OAuth (If Using)
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to **APIs & Services** → **Credentials**
3. Find your OAuth 2.0 Client ID
4. Click **Edit**
5. Add to **Authorized redirect URIs**:
   ```
   https://hfsazlirxtjbarftyoqh.supabase.co/auth/v1/callback
   https://your-vercel-url.vercel.app
   ```
6. Click **Save**

---

### **STEP 5: Test Everything**

#### 5.1 Test Backend API
```bash
# Health check
curl https://web-scraping-7dzj.onrender.com/health

# Should return: {"status": "healthy", ...}
```

#### 5.2 Test Frontend
1. Visit your Vercel URL
2. Open browser DevTools (F12) → Console tab
3. Check for:
   - ✅ No CORS errors
   - ✅ API calls working
   - ✅ Supabase client initialized

#### 5.3 Test Authentication
1. Click **Login** button
2. Try Google OAuth
3. Should redirect to Supabase → Google → back to your site
4. Check if user is logged in

#### 5.4 Test Announcements
1. Navigate to announcements page
2. Select a source (e.g., CBSE)
3. Should load announcements from Render backend
4. Check browser Network tab for API calls

---

## 🎉 Success Checklist

- [ ] Backend deployed to Render and accessible
- [ ] Frontend deployed to Vercel and accessible
- [ ] Frontend can connect to backend (no CORS errors)
- [ ] Supabase redirect URLs updated
- [ ] Google OAuth redirect URLs updated
- [ ] Authentication working
- [ ] Announcements loading from API
- [ ] No console errors in browser

---

## 🐛 Troubleshooting

### Problem: Frontend can't connect to backend

**Symptoms:**
- CORS errors in browser console
- Network requests failing
- "Failed to fetch" errors

**Solutions:**
1. **Check API URL**: Verify meta tag in HTML:
   ```html
   <meta name="api-base-url" content="https://web-scraping-7dzj.onrender.com">
   ```

2. **Check Render backend**: Visit `https://web-scraping-7dzj.onrender.com/health`
   - If it's spinning up, wait 30-50 seconds (free tier)

3. **Check CORS**: Backend should allow all origins (already configured)

4. **Check browser console**: Look for specific error messages

### Problem: Authentication not working

**Symptoms:**
- Login button does nothing
- Redirect errors
- "Redirect URL not allowed" errors

**Solutions:**
1. **Check Supabase redirect URLs**:
   - Go to Supabase Dashboard → Authentication → URL Configuration
   - Add your Vercel URL to both Site URL and Redirect URLs

2. **Check Google OAuth**:
   - Verify redirect URI in Google Cloud Console
   - Should include: `https://hfsazlirxtjbarftyoqh.supabase.co/auth/v1/callback`

3. **Clear browser cache**:
   - Hard refresh (Ctrl+Shift+R)
   - Clear cookies for your site

### Problem: Render backend spinning down

**Symptoms:**
- First request takes 50+ seconds
- "Service unavailable" errors
- Backend works after first request

**Solutions:**
1. **This is normal for free tier**: Render free tier spins down after 15 min inactivity
2. **Upgrade to paid tier**: $7/month for always-on service
3. **Keep it warm**: Set up a cron job to ping your backend every 10 minutes

### Problem: Vercel deployment fails

**Symptoms:**
- Build fails
- "Directory not found" errors

**Solutions:**
1. **Check Root Directory**: Must be set to `frontend`
2. **Check file structure**: Make sure `frontend/` folder exists
3. **Check build logs**: Look for specific error messages

---

## 📊 Your Final URLs

After deployment, you'll have:

- **Backend API**: `https://web-scraping-7dzj.onrender.com`
- **Frontend**: `https://your-project.vercel.app`
- **Database**: Supabase (already configured)
- **Authentication**: Supabase Auth

---

## 🚀 Next Steps (Optional)

### 1. Custom Domain
- Add custom domain in Vercel settings
- Update Supabase redirect URLs with new domain

### 2. Upgrade Render (Recommended)
- Free tier spins down after inactivity
- Upgrade to **Starter** ($7/month) for always-on service
- Better performance and reliability

### 3. Set Up Monitoring
- Use Render logs for backend monitoring
- Use Vercel Analytics for frontend monitoring
- Set up error tracking (Sentry, etc.)

### 4. Optimize Performance
- Enable Vercel caching
- Optimize images
- Use CDN for static assets

---

## 💰 Cost Summary

| Service | Plan | Monthly Cost |
|--------|------|--------------|
| **Render** | Free | $0 (or $7 for paid) |
| **Vercel** | Free | $0 |
| **Supabase** | Free | $0 |
| **Total** | | **$0-7/month** |

**Very affordable!** 🎉

---

## ✅ You're All Set!

Your GETNOTIFY app is now live on the internet! 🚀

**Need help?** Check the troubleshooting section or review the logs in Render/Vercel dashboards.

Good luck! 🎉
