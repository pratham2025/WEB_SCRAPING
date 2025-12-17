# notify_subscribers.py — Email notification service for subscribers

import os
import logging
from typing import List, Dict, Any
from urllib.parse import quote_plus
from dotenv import load_dotenv
from supabase import create_client, Client
from send_email import send_email

# Load environment variables
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - [%(filename)s] - %(message)s")

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Website base URL for CTA links in emails
WEBSITE_BASE_URL = os.getenv("WEBSITE_BASE_URL", "https://getnotify.in")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("❌ Missing Supabase credentials. Please check your .env file.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_subscribers_for_source(source: str) -> List[Dict[str, Any]]:
    """Get all subscribers for a given source."""
    try:
        res = supabase.table("subscriptions") \
            .select("email") \
            .eq("source", source) \
            .execute()
        return res.data or []
    except Exception as e:
        logging.error(f"❌ Failed to fetch subscribers for {source}: {e}")
        return []


def send_notification_email(to_email: str, source: str, announcements: List[Dict[str, Any]]) -> bool:
    """Send a simple email notification to a subscriber about new announcements."""
    try:
        if not announcements:
            return False
        
        # Basic info
        source_name = source
        announcement_count = len(announcements)

        # Build a simple link to your website, optionally including the source
        source_param = quote_plus(source_name)
        website_link = f"{WEBSITE_BASE_URL}?source={source_param}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #12b76a 0%, #0d9d5a 100%); color: white; padding: 24px; border-radius: 8px 8px 0 0; }}
                .content {{ background: #fff; padding: 24px; border: 1px solid #e5e5e5; border-top: none; border-radius: 0 0 8px 8px; }}
                .footer {{ margin-top: 24px; padding-top: 16px; border-top: 1px solid #e5e5e5; font-size: 12px; color: #666; text-align: center; }}
                .button {{ display: inline-block; padding: 10px 18px; background: #12b76a; color: #fff !important; text-decoration: none; border-radius: 999px; font-weight: 600; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0; font-size: 24px;">🔔 New updates from {source_name}</h1>
                </div>
                <div class="content">
                    <p>Hey there,</p>
                    <p><strong>{source_name}</strong> has <strong>{announcement_count} new announcement(s)</strong>.</p>
                    <p>Click the button below to see what announcements have been made on GETNOTIFY.</p>
                    <p style="margin-top: 20px;">
                        <a href="{website_link}" class="button" target="_blank" rel="noopener noreferrer">
                            View announcements
                        </a>
                    </p>
                </div>
                <div class="footer">
                    <p>You're receiving this because you subscribed to {source_name} notifications.</p>
                    <p>To unsubscribe, visit GETNOTIFY and manage your subscriptions.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Send email using the email service
        subject = f"{announcement_count} new announcement(s) from {source_name}"
        success = send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content
        )
        
        if success:
            logging.info(f"✅ Email sent to {to_email} for {source}")
        else:
            logging.warning(f"⚠️ Failed to send email to {to_email} for {source}")
        
        return success
            
    except Exception as e:
        logging.error(f"❌ Failed to send email to {to_email}: {e}")
        return False


def notify_subscribers(source: str, new_announcements: List[Dict[str, Any]]) -> int:
    """Notify all subscribers of a source about new announcements."""
    if not new_announcements:
        return 0
    
    subscribers = get_subscribers_for_source(source)
    if not subscribers:
        logging.info(f"ℹ️ No subscribers for {source}")
        return 0
    
    emails_sent = 0
    for subscriber in subscribers:
        email = subscriber.get("email")
        if email:
            if send_notification_email(email, source, new_announcements):
                emails_sent += 1
    
    logging.info(f"✅ Notified {emails_sent}/{len(subscribers)} subscribers for {source}")
    return emails_sent

