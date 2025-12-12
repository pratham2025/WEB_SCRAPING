# Mobile Access Login Fix

## Problem
When accessing the site from a mobile device using an IP address (e.g., `http://197.168.31.200:5501`), the Google login doesn't work.

## Root Cause
The OAuth redirect URL must be whitelisted in both:
1. **Supabase Dashboard** - Authentication settings
2. **Google Cloud Console** - OAuth 2.0 Client settings

## Solution

### Step 1: Add Redirect URL to Supabase

1. Go to your Supabase Dashboard: https://supabase.com/dashboard
2. Select your project
3. Navigate to: **Authentication** → **URL Configuration**
4. In the **Redirect URLs** section, add:
   ```
   http://197.168.31.200:5501/*
   http://197.168.31.200:5501/index.html
   http://197.168.31.200:5501/home.html
   ```
   (Replace `197.168.31.200:5501` with your actual IP and port)

5. Also add the Site URL if not already set:
   ```
   http://197.168.31.200:5501
   ```

### Step 2: Add Redirect URI to Google Cloud Console

1. Go to Google Cloud Console: https://console.cloud.google.com
2. Select your project
3. Navigate to: **APIs & Services** → **Credentials**
4. Find your OAuth 2.0 Client ID (the one used by Supabase)
5. Click **Edit**
6. In **Authorized redirect URIs**, add:
   ```
   https://hfsazlirxtjbarftyoqh.supabase.co/auth/v1/callback
   ```
   (This is your Supabase project's callback URL - it should already be there)

   **Note:** Supabase handles the redirect, so you only need the Supabase callback URL, not your local IP.

### Step 3: Verify Supabase Site URL

1. In Supabase Dashboard → **Authentication** → **URL Configuration**
2. Check **Site URL** - it should be set to your production domain OR you can use:
   ```
   http://localhost:5501
   ```
   (For development, Supabase allows localhost by default)

### Step 4: Test the Login

1. Open your site on mobile: `http://197.168.31.200:5501`
2. Open browser console (if possible) or check network tab
3. Click "Login" button
4. Check console for debug messages showing the redirect URL
5. The redirect URL should be: `http://197.168.31.200:5501/index.html` (or current page)

## Common Issues

### Issue: "redirect_uri_mismatch" error
**Solution:** Make sure the redirect URL in the error message is added to Supabase's Redirect URLs list.

### Issue: Login button does nothing
**Solution:** 
- Check browser console for errors
- Verify Supabase client is initialized (should see "✅ Supabase client initialized" in console)
- Check if `secrets.js` is loaded before `auth.js`

### Issue: Redirects but shows error
**Solution:**
- Check the exact error message in the alert
- Verify the redirect URL matches what's configured in Supabase
- Make sure your IP address is accessible from your mobile device (same network)

## Debugging

The updated `auth.js` now includes detailed logging. When you click login, check the browser console for:
- Current URL
- Redirect URL being used
- Any error messages

## Alternative: Use ngrok for Testing

If you continue having issues with IP addresses, consider using ngrok:

1. Install ngrok: https://ngrok.com
2. Run: `ngrok http 5501`
3. Use the ngrok URL (e.g., `https://abc123.ngrok.io`) instead of IP
4. Add this URL to Supabase and Google OAuth settings

This provides a stable HTTPS URL that works better with OAuth.
