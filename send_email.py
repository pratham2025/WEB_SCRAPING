"""
send_email.py — Email service using SMTP (ZeptoMail-ready)

This module is now aligned with your ZeptoMail test in `test_mail.py`.
It uses standard smtplib + EmailMessage and reads all credentials from env.
"""

import os
import traceback
import logging
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - [%(filename)s] - %(message)s")

# Configuration - generic SMTP (defaults set up for ZeptoMail)
SMTP_EMAIL = os.getenv("SMTP_EMAIL", "emailapikey")  # ZeptoMail recommends "emailapikey" as username
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")           # Set your ZeptoMail API key here
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.zeptomail.in")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
FROM_EMAIL = os.getenv("FROM_EMAIL", "alerts@getnotify.in")

if not SMTP_EMAIL or not SMTP_PASSWORD:
    logging.warning("⚠️ SMTP_EMAIL or SMTP_PASSWORD not found in environment variables.")


def send_email(to_email: str, subject: str, html_content: str, from_email: str = None, debug: bool = False) -> bool:
    """
    Send an email using generic SMTP (ZeptoMail / others).

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
        # Build email message
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = to_email
        # Set HTML body
        msg.set_content("This email requires an HTML-capable client.")
        msg.add_alternative(html_content, subtype="html")

        if SMTP_PORT == 465:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
                server.login(SMTP_EMAIL, SMTP_PASSWORD)
                server.send_message(msg)
        else:
            # Default path for ZeptoMail: port 587 + STARTTLS
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls(context=ssl.create_default_context())
                server.login(SMTP_EMAIL, SMTP_PASSWORD)
                server.send_message(msg)

        if debug:
            print("SUCCESS: Email sent successfully via SMTP. Check inbox/spam.")
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
    """Local test function to send a test email using current SMTP settings."""
    TO = os.getenv("TEST_EMAIL_TO", "prathmeshpatiltoi@gmail.com")

    send_email(
        to_email=TO,
        subject="GETNOTIFY — test email via SMTP (ZeptoMail)",
        html_content="<strong>Hello from GETNOTIFY — test email via ZeptoMail SMTP</strong>",
        debug=True,
    )


if __name__ == "__main__":
    main()
