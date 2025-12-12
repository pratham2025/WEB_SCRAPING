# ⚡ Quick Setup: getnotify.in Domain

## ✅ Yes! Your domain will show on the internet once configured

After setup (15-30 minutes), your site will be live at:
- **Frontend**: `https://getnotify.in`
- **Backend API**: `https://api.getnotify.in`

---

## 🚀 Quick Steps (30 minutes)

### 1. Add Domain to Vercel (5 min)
1. Vercel Dashboard → Your Project → **Settings** → **Domains**
2. Click **"Add Domain"**
3. Enter: `getnotify.in`
4. Copy the DNS records shown

### 2. Add Domain to Render (5 min)
1. Render Dashboard → Your Service → **Settings** → **Custom Domain**
2. Click **"Add Custom Domain"**
3. Enter: `api.getnotify.in`
4. Copy the CNAME record shown

### 3. Add DNS Records (10 min)
1. Go to your domain registrar (where you bought the domain)
2. Find **DNS Management** or **DNS Settings**
3. Add these records:

```
Type    Name    Value
─────────────────────────────────────────────
A       @       [IP from Vercel]
CNAME   www     [value from Vercel]
CNAME   api     web-scraping-7dzj.onrender.com
```

4. Save and wait 15-30 minutes for DNS to propagate

### 4. Update Code (5 min)
After DNS propagates, update your frontend files:
- Change API URL from `https://web-scraping-7dzj.onrender.com` 
- To: `https://api.getnotify.in`

### 5. Update Supabase (5 min)
1. Supabase Dashboard → **Authentication** → **URL Configuration**
2. Update **Site URL** to: `https://getnotify.in`
3. Add redirect URLs: `https://getnotify.in`, `https://www.getnotify.in`

---

## 📖 Full Guide

See `CUSTOM_DOMAIN_SETUP.md` for detailed step-by-step instructions with screenshots guidance.

---

## ⏱️ Timeline

- **Setup Time**: 30 minutes
- **DNS Propagation**: 15-30 minutes (can take up to 48 hours)
- **SSL Certificates**: Automatic (free from Vercel & Render)
- **Total**: ~1 hour to go live

---

## ✅ Checklist

- [ ] Domain added to Vercel
- [ ] Domain added to Render (as `api.getnotify.in`)
- [ ] DNS records added
- [ ] DNS propagated (check at whatsmydns.net)
- [ ] Frontend code updated
- [ ] Supabase URLs updated
- [ ] Test site at `https://getnotify.in`

---

## 🎉 Result

Once done, your site will be accessible at:
- **Main Site**: `https://getnotify.in`
- **API**: `https://api.getnotify.in`

Your GETNOTIFY app will be live on the internet with your custom domain! 🚀
