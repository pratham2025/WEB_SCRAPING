# 🚀 Step-by-Step: Deploy Frontend to Vercel

## ✅ Step 1: Update Frontend to Use Your Render API

Your backend is live at: **`https://web-scraping-7dzj.onrender.com`**

I'll update your HTML files to use this URL. Then you'll deploy to Vercel.

---

## ✅ Step 2: Push Code to GitHub

Make sure your code is pushed to GitHub:

```bash
git add .
git commit -m "Configure API URL for Render backend"
git push origin master
```

---

## ✅ Step 3: Deploy to Vercel

### 3.1 Go to Vercel
1. Visit [vercel.com](https://vercel.com)
2. Sign up/Login with GitHub

### 3.2 Import Your Project
1. Click **"Add New Project"**
2. Select your **`WEB_SCRAPING`** repository
3. Click **"Import"**

### 3.3 Configure Project Settings
**Important Settings:**
- **Framework Preset**: `Other` (or leave blank)
- **Root Directory**: `frontend` ⚠️ **IMPORTANT!**
- **Build Command**: (leave empty - no build needed)
- **Output Directory**: `.` (current directory)
- **Install Command**: (leave empty)

### 3.4 Add Environment Variables (Optional)
You can add these if needed:
- `NEXT_PUBLIC_API_URL=https://web-scraping-7dzj.onrender.com`

### 3.5 Deploy!
1. Click **"Deploy"**
2. Wait 1-2 minutes
3. Your site will be live at: `https://your-project.vercel.app`

---

## ✅ Step 4: Update Supabase Redirect URLs

### 4.1 Go to Supabase Dashboard
1. Visit [supabase.com/dashboard](https://supabase.com/dashboard)
2. Select your project

### 4.2 Update Authentication Settings
1. Go to **Authentication** → **URL Configuration**
2. Update **Site URL** to your Vercel URL:
   ```
   https://your-project.vercel.app
   ```

3. Add **Redirect URLs**:
   ```
   https://your-project.vercel.app
   https://your-project.vercel.app/auth/callback
   https://web-scraping-7dzj.onrender.com
   ```

### 4.3 Update Google OAuth (if using)
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to **APIs & Services** → **Credentials**
3. Edit your OAuth 2.0 Client
4. Add **Authorized redirect URIs**:
   ```
   https://hfsazlirxtjbarftyoqh.supabase.co/auth/v1/callback
   https://your-project.vercel.app
   ```

---

## ✅ Step 5: Test Your Deployment

### Test Backend:
```bash
curl https://web-scraping-7dzj.onrender.com/health
curl https://web-scraping-7dzj.onrender.com/sources
```

### Test Frontend:
1. Visit your Vercel URL
2. Open browser console (F12)
3. Check for errors
4. Test login functionality
5. Test fetching announcements

---

## 🎉 You're Done!

Your app is now live:
- **Backend**: `https://web-scraping-7dzj.onrender.com`
- **Frontend**: `https://your-project.vercel.app`
- **Database**: Supabase (already configured)

---

## 🐛 Troubleshooting

### Frontend can't connect to backend:
- Check browser console for CORS errors
- Verify API URL is correct in HTML meta tag
- Check Render backend is running (visit `/health` endpoint)

### Authentication not working:
- Verify Supabase redirect URLs are updated
- Check Google OAuth redirect URLs
- Clear browser cache and cookies

### Render backend spinning down:
- Free tier spins down after 15 min inactivity
- First request may take 50 seconds
- Consider upgrading to paid tier ($7/month) for always-on

---

## 📝 Next Steps

1. ✅ Test all features
2. ✅ Set up custom domain (optional)
3. ✅ Monitor Render logs
4. ✅ Set up error tracking (optional)
5. ✅ Consider upgrading Render to paid tier

Good luck! 🚀
