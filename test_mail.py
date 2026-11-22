import os
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

port = int(os.getenv("SMTP_PORT", "587"))
smtp_server = os.getenv("SMTP_HOST", "smtp.zeptomail.in")
username = os.getenv("SMTP_EMAIL", "emailapikey")
password = os.getenv("SMTP_PASSWORD")
from_email = os.getenv("FROM_EMAIL", "alerts@getnotify.in")
to_email = os.getenv("TEST_EMAIL", from_email)

if not password:
    print("❌ Error: SMTP_PASSWORD is not set. Please set it in your environment or .env file.")
    exit(1)

message = "Test email sent successfully."
msg = EmailMessage()
msg['Subject'] = "Test Email"
msg['From'] = from_email
msg['To'] = to_email
msg.set_content(message)

try:
    if port == 465:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(username, password)
            server.send_message(msg)
    elif port == 587:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
    else:
        print("use 465 / 587 as port value")
        exit(1)
    print("successfully sent")
except Exception as e:
    print(e)
