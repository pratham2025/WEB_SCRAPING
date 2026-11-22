# Google OAuth Setup Guide

## Error: "no registered origin" / "Error 401: invalid_client"

This error occurs when Google OAuth is not properly configured. Follow these steps:

## Step 1: Configure Supabase Dashboard

1. Go to your Supabase project: https://hfsazlirxtjbarftyoqh.supabase.co
2. Navigate to **Authentication** → **Providers**
3. Enable **Google** provider
4. Enter your Google OAuth credentials:
   - **Client ID**: `688906729987-opjalg044vu4f7u7obk3rkgi4cr345sl.apps.googleusercontent.com`
   - **Client Secret**: `YOUR_GOOGLE_CLIENT_SECRET`
5. Go to **Authentication** → **URL Configuration**
6. Set **Site URL** to your frontend URL:
   - For local development: `http://localhost:5500` (or your port)
   - For production: `https://yourdomain.com`
7. Add **Redirect URLs** (add all variations you might use):
   - `http://localhost:5500/frontend/home.html`
   - `http://127.0.0.1:5500/frontend/home.html`
   - `https://yourdomain.com/frontend/home.html`

## Step 2: Configure Google Cloud Console

⚠️ **IMPORTANT**: You have TWO Google OAuth Client IDs. You need to configure BOTH:

### For Supabase OAuth (Client ID: `688906729987-opjalg044vu4f7u7obk3rkgi4cr345sl`):

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select project: `sharp-harbor-477312-g9`
3. Navigate to **APIs & Services** → **Credentials**
4. Find your OAuth 2.0 Client ID: `688906729987-opjalg044vu4f7u7obk3rkgi4cr345sl`
5. Click **Edit**
6. Under **Authorized redirect URIs**, add:
   - `https://hfsazlirxtjbarftyoqh.supabase.co/auth/v1/callback`
   - (This is the Supabase callback URL - REQUIRED)
7. Under **Authorized JavaScript origins**, add:
   - `http://localhost:5500` (for local dev)
   - `http://127.0.0.1:5500` (for local dev)
   - `http://localhost:5501` (if using different port)
   - `http://127.0.0.1:5501` (if using different port)
   - `https://yourdomain.com` (for production)
   - `https://hfsazlirxtjbarftyoqh.supabase.co` (Supabase domain)

### For Old Google Sign-In Button (Client ID: `599841597854-ftnbigq7pfe6h4hdav71v5873n9b8jdn`):

**Option A: Update the old client ID** (if you want to keep both):
1. Find OAuth 2.0 Client ID: `599841597854-ftnbigq7pfe6h4hdav71v5873n9b8jdn`
2. Click **Edit**
3. Under **Authorized JavaScript origins**, add the SAME origins as above:
   - `http://localhost:5500`
   - `http://127.0.0.1:5500`
   - (Add all the origins you're using)

**Option B: Remove the old Google Sign-In** (Recommended):
- Replace the old Google Sign-In button in the header modal with the new Supabase OAuth button
- This way you only need to configure one client ID

## Step 3: Verify Configuration

After making changes:
1. Wait 1-2 minutes for changes to propagate
2. Clear browser cache
3. Try logging in again

## Common Issues

- **"[GSI_LOGGER]: The given origin is not allowed"**: 
  - The current page origin (e.g., `http://localhost:5500`) is not in Google's authorized JavaScript origins
  - **Solution**: Add your current origin to BOTH client IDs in Google Cloud Console
  - To find your current origin, check the browser console or look at the URL bar

- **"no registered origin"**: The current page URL is not in Google's authorized origins
- **"invalid_client"**: Client ID/Secret mismatch between Supabase and Google Console
- **Redirect loop**: Site URL in Supabase doesn't match your actual frontend URL

## Quick Fix for Current Error

The error `[GSI_LOGGER]: The given origin is not allowed` means:
1. Check what origin you're currently using (look at your browser URL - e.g., `http://localhost:5500`)
2. Go to Google Cloud Console → Credentials
3. Edit Client ID: `599841597854-ftnbigq7pfe6h4hdav71v5873n9b8jdn`
4. Add your current origin to **Authorized JavaScript origins**
5. Save and wait 1-2 minutes
6. Refresh the page

## Testing

1. Open browser console (F12)
2. Check for any error messages
3. Verify `window.supabase` is defined: `console.log(window.supabase)`
4. Try login and check network tab for OAuth requests

