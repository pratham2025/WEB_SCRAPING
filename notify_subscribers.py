# notify_subscribers.py — Email notification service for subscribers

import os
import logging
from typing import List, Dict, Any
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
    """Send email notification to a subscriber about new announcements."""
    try:
        if not announcements:
            return False
        
        # Build email content
        source_name = source
        announcement_count = len(announcements)
        
        # Create HTML email content
        announcements_html = ""
        for ann in announcements[:10]:  # Limit to 10 most recent
            text = ann.get("text", "New announcement")
            link = ann.get("link", "#")
            announcements_html += f"""
            <div style="margin-bottom: 16px; padding: 12px; background: #f7fff9; border-left: 3px solid #12b76a; border-radius: 4px;">
                <p style="margin: 0 0 8px 0; font-weight: 600; color: #1a1a1a;">{text}</p>
                <a href="{link}" style="color: #12b76a; text-decoration: none; font-size: 14px;">View announcement →</a>
            </div>
            """
        
        if len(announcements) > 10:
            announcements_html += f'<p style="color: #666; font-size: 14px; margin-top: 12px;">... and {len(announcements) - 10} more announcements</p>'
        
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
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0; font-size: 24px;">🔔 New Announcements from {source_name}</h1>
                </div>
                <div class="content">
                    <p>Hello,</p>
                    <p>We found <strong>{announcement_count} new announcement(s)</strong> from <strong>{source_name}</strong>:</p>
                    {announcements_html}
                    <div style="margin-top: 24px; padding: 16px; background: #f0f9ff; border-radius: 4px;">
                        <p style="margin: 0; font-size: 14px; color: #1e40af;">
                            <strong>💡 Tip:</strong> Visit <a href="http://localhost:8000" style="color: #12b76a;">GETNOTIFY</a> to see all announcements and manage your subscriptions.
                        </p>
                    </div>
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
        subject = f"🔔 {announcement_count} New Announcement(s) from {source_name}"
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

