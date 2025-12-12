# 🔐 Fix Login Issue: getnotify.in

## 🐛 Problem

Users can't login because:
- Google OAuth redirect shows: `hfsazlirxtjbarftyoqh.supabase.co` (Supabase project URL)
- Should show: `getnotify.in` (your custom domain)
- Redirect URLs are not configured for your custom domain

---

## ✅ Quick Fix (5 minutes)

### **STEP 1: Update Supabase Site URL**

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to **Authentication** → **URL Configuration**
4. Update **Site URL**:
   ```
   https://getnotify.in
   ```
   (Remove any old URLs like `localhost` or Vercel URLs)

5. In **Redirect URLs**, add these (one per line):
   ```
   https://getnotify.in
   https://www.getnotify.in
   https://getnotify.in/**
   https://www.getnotify.in/**
   https://hfsazlirxtjbarftyoqh.supabase.co/auth/v1/callback
   ```

6. Click **Save**

---

### **STEP 2: Update Google OAuth Redirect URIs**

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to **APIs & Services** → **Credentials**
3. Find your OAuth 2.0 Client ID (the one you're using)
4. Click **Edit** (pencil icon)
5. In **Authorized redirect URIs**, add these:
   ```
   https://hfsazlirxtjbarftyoqh.supabase.co/auth/v1/callback
   https://getnotify.in
   https://www.getnotify.in
   ```
   ⚠️ **Keep the Supabase callback URL** - it's required!

6. Click **Save**

---

### **STEP 3: Clear Browser Cache**

1. Open your site: `https://getnotify.in`
2. Press `Ctrl + Shift + Delete` (or `Cmd + Shift + Delete` on Mac)
3. Select **"Cached images and files"**
4. Click **"Clear data"**
5. Or use **Incognito/Private mode** to test

---

### **STEP 4: Test Login**

1. Visit `https://getnotify.in`
2. Click **Login** button
3. You should see Google login page
4. After selecting account, it should redirect back to `getnotify.in` (not Supabase URL)

---

## 🎯 What Should Happen

**Before Fix:**
```
User clicks Login → Google → "to continue to hfsazlirxtjbarftyoqh.supabase.co" ❌
```

**After Fix:**
```
User clicks Login → Google → "to continue to getnotify.in" ✅
→ Redirects back to https://getnotify.in ✅
```

---

## 🐛 Still Not Working?

### Check 1: Verify Supabase Configuration
- Go to Supabase Dashboard → Authentication → URL Configuration
- **Site URL** must be: `https://getnotify.in`
- **Redirect URLs** must include: `https://getnotify.in`

### Check 2: Verify Google OAuth
- Go to Google Cloud Console → Credentials
- **Authorized redirect URIs** must include:
  - `https://hfsazlirxtjbarftyoqh.supabase.co/auth/v1/callback` (required!)
  - `https://getnotify.in`
  - `https://www.getnotify.in`

### Check 3: Check Browser Console
1. Open `https://getnotify.in`
2. Press `F12` → **Console** tab
3. Click Login
4. Look for errors
5. Common errors:
   - `redirect_uri_mismatch` → Google OAuth not configured
   - `invalid_client` → OAuth client ID wrong
   - CORS errors → Supabase redirect URLs wrong

### Check 4: Test in Incognito
- Open Incognito/Private window
- Visit `https://getnotify.in`
- Try login
- This bypasses cache issues

---

## 📝 Complete Checklist

- [ ] Supabase Site URL = `https://getnotify.in`
- [ ] Supabase Redirect URLs include `https://getnotify.in`
- [ ] Google OAuth includes `https://getnotify.in`
- [ ] Google OAuth includes Supabase callback URL
- [ ] Browser cache cleared
- [ ] Tested in Incognito mode
- [ ] No console errors

---

## ⚡ Quick Test

After making changes, test with this:

1. **Open Incognito window**
2. Visit: `https://getnotify.in`
3. Click **Login**
4. **Check the Google page** - should say "to continue to **getnotify.in**"
5. Select account
6. Should redirect back to `https://getnotify.in`

---

## 🎉 Success!

Once fixed, users will see:
- Google login page shows: "to continue to **getnotify.in**" ✅
- After login, redirects to: `https://getnotify.in` ✅
- User is logged in ✅

---

## 💡 Important Notes

1. **Supabase callback URL is required**: Keep `https://hfsazlirxtjbarftyoqh.supabase.co/auth/v1/callback` in Google OAuth - it's how Supabase handles the OAuth flow

2. **Both URLs needed**: You need BOTH:
   - Your custom domain (`getnotify.in`) - for user experience
   - Supabase callback URL - for OAuth to work

3. **Wait a few minutes**: Changes can take 1-5 minutes to propagate

4. **Clear cache**: Always clear browser cache after making changes

---

If it's still not working after these steps, let me know what error you see! 🚀
