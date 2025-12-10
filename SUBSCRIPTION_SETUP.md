# Subscription Feature Setup Guide

This guide will help you set up the email subscription feature for GETNOTIFY.

## Prerequisites

1. **Supabase Database**: Make sure you have a Supabase project set up
2. **SendGrid Account**: You need a SendGrid API key (already configured in `sendgrid.env`)
3. **Python Dependencies**: Ensure all required packages are installed

## Setup Steps

### 1. Create Subscriptions Table in Supabase

Run the SQL script in your Supabase SQL Editor:

```sql
-- See create_subscriptions_table.sql for the complete SQL
```

Or manually create the table:
- Go to your Supabase Dashboard
- Navigate to SQL Editor
- Run the SQL from `create_subscriptions_table.sql`

The table structure:
- `id` (BIGSERIAL PRIMARY KEY)
- `email` (TEXT NOT NULL)
- `source` (TEXT NOT NULL)
- `created_at` (TIMESTAMPTZ DEFAULT NOW())
- UNIQUE constraint on (email, source)

### 2. Verify Environment Variables

Make sure your `.env` file contains:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SENDGRID_API_KEY` (or load from `sendgrid.env`)

### 3. Test the Feature

1. **Start the API server**:
   ```bash
   uvicorn scraper_api:app --reload --port 8000
   ```

2. **Test subscription endpoint**:
   ```bash
   curl -X POST http://localhost:8000/subscribe \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "source": "CBSE"}'
   ```

3. **Check subscriptions**:
   ```bash
   curl http://localhost:8000/subscriptions?email=test@example.com
   ```

4. **Test email notification**:
   - Run a scraper for a source you're subscribed to
   - Check if new announcements trigger email notifications

## How It Works

1. **User subscribes**: User clicks "Subscribe" button on a source card
2. **Subscription stored**: Email and source are saved in Supabase `subscriptions` table
3. **Scraper runs**: When scraper finds new announcements, it calls `notify_subscribers()`
4. **Emails sent**: All subscribers for that source receive an email with new announcements

## Frontend Features

- **Subscribe Button**: Added to each source card
- **Visual Feedback**: Button shows "✓ Subscribed" when active
- **Login Required**: Users must be logged in to subscribe
- **Auto-refresh**: Subscription status updates automatically

## API Endpoints

- `POST /subscribe` - Subscribe to a source
- `POST /unsubscribe` - Unsubscribe from a source
- `GET /subscriptions?email=<email>` - Get all subscriptions for a user

## Email Notifications

- Sent via SendGrid
- HTML formatted emails
- Includes up to 10 most recent announcements
- Includes link to view all announcements

## Troubleshooting

1. **Emails not sending**: Check SendGrid API key and verify sender email
2. **Subscriptions not saving**: Verify Supabase table exists and RLS policies allow inserts
3. **Button not showing**: Check browser console for JavaScript errors
4. **API errors**: Check API logs for detailed error messages

## Next Steps

- Add unsubscribe link in emails
- Add email preferences (frequency, digest mode)
- Add subscription management page
- Add email verification for new subscriptions

