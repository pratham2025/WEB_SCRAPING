# 🌐 Custom Domain Setup: getnotify.in

## ✅ What You'll Get

After setup:
- **Frontend**: `https://getnotify.in` (or `https://www.getnotify.in`)
- **Backend API**: `https://api.getnotify.in` (optional subdomain)
- **Fully branded** with your domain!

---

## 🚀 Step-by-Step Setup

### **STEP 1: Configure Domain on Vercel (Frontend)**

#### 1.1 Add Domain in Vercel
1. Go to your Vercel project dashboard
2. Click **"Settings"** tab
3. Click **"Domains"** in the left sidebar
4. Click **"Add Domain"**
5. Enter: `getnotify.in`
6. Click **"Add"**

#### 1.2 Add WWW Subdomain (Optional but Recommended)
1. In the same Domains page
2. Click **"Add Domain"** again
3. Enter: `www.getnotify.in`
4. Click **"Add"**

#### 1.3 Get DNS Records from Vercel
Vercel will show you DNS records to add. You'll see something like:

**For getnotify.in:**
- **Type**: `A`
- **Name**: `@` (or blank)
- **Value**: `76.76.21.21` (Vercel's IP - they'll provide the actual IP)

**For www.getnotify.in:**
- **Type**: `CNAME`
- **Name**: `www`
- **Value**: `cname.vercel-dns.com` (Vercel will provide exact value)

**⚠️ Don't add these yet!** We'll do DNS configuration in Step 3.

---

### **STEP 2: Configure Domain on Render (Backend API)**

#### Option A: Use Subdomain (Recommended)
Use `api.getnotify.in` for your backend:

1. Go to Render dashboard → Your service (`WEB_SCRAPING`)
2. Click **"Settings"** tab
3. Scroll to **"Custom Domain"** section
4. Click **"Add Custom Domain"**
5. Enter: `api.getnotify.in`
6. Click **"Save"**

Render will show you DNS records:
- **Type**: `CNAME`
- **Name**: `api`
- **Value**: `web-scraping-7dzj.onrender.com` (or similar)

#### Option B: Use Main Domain (Alternative)
If you want `getnotify.in/api` instead:
- This requires more complex setup (reverse proxy)
- **Not recommended** - subdomain is easier

---

### **STEP 3: Configure DNS Records**

Go to your domain registrar (where you bought `getnotify.in`) and add DNS records:

#### 3.1 Find Your DNS Settings
- Log into your domain registrar (GoDaddy, Namecheap, etc.)
- Find **"DNS Management"** or **"DNS Settings"**
- Look for **"DNS Records"** or **"Manage DNS"**

#### 3.2 Add Records

**For Frontend (Vercel):**

| Type | Name | Value | TTL |
|------|------|-------|-----|
| `A` | `@` (or blank) | `76.76.21.21` | Auto |
| `CNAME` | `www` | `cname.vercel-dns.com` | Auto |

**For Backend (Render):**

| Type | Name | Value | TTL |
|------|------|-------|-----|
| `CNAME` | `api` | `web-scraping-7dzj.onrender.com` | Auto |

**Example DNS Records Table:**
```
Type    Name    Value                                    TTL
─────────────────────────────────────────────────────────────
A       @       76.76.21.21                              Auto
CNAME   www     cname.vercel-dns.com                     Auto
CNAME   api     web-scraping-7dzj.onrender.com           Auto
```

#### 3.3 Save DNS Records
- Click **"Save"** or **"Update"**
- DNS propagation takes **5 minutes to 48 hours** (usually 15-30 minutes)

---

### **STEP 4: Update Frontend Code**

Once your domain is live, update the API URL in your frontend:

#### 4.1 Update HTML Files
Update `frontend/index.html` and `frontend/home.html`:

**Change from:**
```html
<meta name="api-base-url" content="https://web-scraping-7dzj.onrender.com">
```

**Change to:**
```html
<meta name="api-base-url" content="https://api.getnotify.in">
```

#### 4.2 Push to GitHub
```bash
git add frontend/index.html frontend/home.html
git commit -m "Update API URL to custom domain"
git push origin master
```

Vercel will auto-deploy the changes.

---

### **STEP 5: Update Supabase Configuration**

#### 5.1 Update Site URL
1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to **Authentication** → **URL Configuration**
4. Update **Site URL**:
   ```
   https://getnotify.in
   ```

#### 5.2 Update Redirect URLs
Add these redirect URLs:
```
https://getnotify.in
https://www.getnotify.in
https://getnotify.in/auth/callback
https://www.getnotify.in/auth/callback
https://api.getnotify.in
```

#### 5.3 Update Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to **APIs & Services** → **Credentials**
3. Edit your OAuth 2.0 Client
4. Add **Authorized redirect URIs**:
   ```
   https://hfsazlirxtjbarftyoqh.supabase.co/auth/v1/callback
   https://getnotify.in
   https://www.getnotify.in
   ```

---

### **STEP 6: Verify Everything Works**

#### 6.1 Check DNS Propagation
Use these tools to check if DNS is propagated:
- [whatsmydns.net](https://www.whatsmydns.net)
- Enter `getnotify.in` and check A record
- Enter `api.getnotify.in` and check CNAME record

#### 6.2 Test Frontend
1. Visit `https://getnotify.in`
2. Should load your Vercel site
3. Open browser console (F12) - check for errors

#### 6.3 Test Backend
```bash
# Test health endpoint
curl https://api.getnotify.in/health

# Test sources
curl https://api.getnotify.in/sources
```

#### 6.4 Test Full Flow
1. Visit `https://getnotify.in`
2. Try logging in
3. Try fetching announcements
4. Check browser Network tab for API calls to `api.getnotify.in`

---

## 🎯 Final Architecture

After setup, your architecture will be:

```
Users → https://getnotify.in (Vercel Frontend)
              ↓
        API Calls to
              ↓
    https://api.getnotify.in (Render Backend)
              ↓
        Database/Auth
              ↓
        Supabase Cloud
```

---

## ⏱️ Timeline

- **DNS Configuration**: 5-30 minutes
- **Vercel Domain Setup**: Instant (after DNS)
- **Render Domain Setup**: Instant (after DNS)
- **SSL Certificates**: Auto (Vercel & Render provide free SSL)
- **Total Time**: ~30 minutes to 1 hour

---

## 🐛 Troubleshooting

### Problem: Domain not loading

**Check:**
1. DNS propagation: Use [whatsmydns.net](https://www.whatsmydns.net)
2. DNS records: Verify all records are correct
3. Wait time: DNS can take up to 48 hours (usually 15-30 min)

### Problem: SSL Certificate Error

**Solution:**
- Vercel and Render provide free SSL automatically
- Wait 5-10 minutes after DNS propagation
- SSL certificates are issued automatically

### Problem: API calls failing

**Check:**
1. API URL in frontend: Should be `https://api.getnotify.in`
2. CORS: Backend should allow your domain
3. Backend health: Visit `https://api.getnotify.in/health`

### Problem: Authentication not working

**Check:**
1. Supabase redirect URLs: Must include `https://getnotify.in`
2. Google OAuth: Must include your domain
3. Clear browser cache and cookies

---

## 📝 Checklist

- [ ] Domain added to Vercel
- [ ] Domain added to Render (as `api.getnotify.in`)
- [ ] DNS records added at domain registrar
- [ ] DNS propagated (check with whatsmydns.net)
- [ ] Frontend code updated with new API URL
- [ ] Code pushed to GitHub
- [ ] Supabase Site URL updated
- [ ] Supabase Redirect URLs updated
- [ ] Google OAuth redirect URLs updated
- [ ] Frontend accessible at `https://getnotify.in`
- [ ] Backend accessible at `https://api.getnotify.in`
- [ ] Authentication working
- [ ] API calls working

---

## 🎉 You're Done!

Once DNS propagates (15-30 minutes), your site will be live at:
- **Frontend**: `https://getnotify.in`
- **Backend**: `https://api.getnotify.in`

Your GETNOTIFY app will be accessible to the world with your custom domain! 🚀

---

## 💡 Pro Tips

1. **Use www subdomain**: Add `www.getnotify.in` for better SEO
2. **Monitor DNS**: Use [whatsmydns.net](https://www.whatsmydns.net) to track propagation
3. **Test thoroughly**: Test all features after domain setup
4. **Keep backups**: Save your DNS records somewhere safe
5. **SSL is automatic**: Both Vercel and Render provide free SSL certificates

Good luck! 🎉
