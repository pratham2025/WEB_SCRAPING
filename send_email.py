# send_email.py — Email service using Zoho SMTP (yagmail)
import os
import traceback
import logging
import yagmail
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - [%(filename)s] - %(message)s")

# Configuration - Zoho Mail SMTP
SMTP_EMAIL = os.getenv("SMTP_EMAIL", "alerts@getnotify.in")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "vdVgGctmQ5YS")
SMTP_HOST = os.getenv("SMTP_HOST", "smtppro.zoho.in")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
FROM_EMAIL = SMTP_EMAIL  # Default sender email

if not SMTP_EMAIL or not SMTP_PASSWORD:
    logging.warning("⚠️ SMTP_EMAIL or SMTP_PASSWORD not found in environment variables.")


def send_email(to_email: str, subject: str, html_content: str, from_email: str = None, debug: bool = False) -> bool:
    """
    Send an email using Zoho SMTP (yagmail).
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML content of the email
        from_email: Sender email (defaults to FROM_EMAIL)
        debug: If True, print debug information
    
    Returns:
        True if email was sent successfully, False otherwise
    """
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        error_msg = "SMTP_EMAIL or SMTP_PASSWORD environment variable is not set."
        if debug:
            print(f"ERROR: {error_msg}")
            print("Please set SMTP_EMAIL and SMTP_PASSWORD in your .env file")
        logging.error(f"❌ {error_msg}")
        return False
    
    sender = from_email or FROM_EMAIL
    
    if debug:
        print(f"DEBUG: SMTP configuration found? YES")
        print(f"DEBUG: From: {sender}")
        print(f"DEBUG: To: {to_email}")
        print(f"DEBUG: Subject: {subject}")
        print(f"DEBUG: SMTP Host: {SMTP_HOST}:{SMTP_PORT}")
    
    try:
        # Initialize SMTP connection
        yag = yagmail.SMTP(
            user=SMTP_EMAIL,
            password=SMTP_PASSWORD,
            host=SMTP_HOST,
            port=SMTP_PORT,
            smtp_starttls=True,
            smtp_ssl=False
        )
        
        if debug:
            print("DEBUG: Sending email now...")
        
        # Send email with HTML content
        # yagmail automatically detects HTML content when passed as string
        yag.send(
            to=to_email,
            subject=subject,
            contents=html_content
        )
        
        if debug:
            print("SUCCESS: Email sent successfully via Zoho SMTP. Check inbox/spam.")
        logging.info(f"✅ Email sent successfully to {to_email}")
        return True
            
    except Exception as e:
        error_msg = f"Failed to send email to {to_email}: {e}"
        if debug:
            print("EXCEPTION while sending:")
            traceback.print_exc()
        logging.error(f"❌ {error_msg}")
        return False


def main():
    """Test function to send a test email."""
    TO = "prathmeshpatiltoi@gmail.com"  # test sending to yourself
    
    send_email(
        to_email=TO,
        subject="GETNOTIFY — test email",
        html_content="<strong>Hello from GETNOTIFY — test email via Zoho SMTP</strong>",
        debug=True
    )


if __name__ == "__main__":
    main()
