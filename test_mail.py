import yagmail

sender_email = "alerts@getnotify.in"
sender_password = "vdVgGctmQ5YS"  # recommended: use App Password

receiver_email = "prathmeshpatiltoi@gmail.com"  # for testing

subject = "New Announcement Alert"
message = """
Your tracked source has a new announcement.

Click here to view:
https://getnotify.in
"""

# Initialize SMTP connection
yag = yagmail.SMTP(
    user=sender_email,
    password=sender_password,
    host="smtppro.zoho.in",
    port=587,
    smtp_starttls=True,
    smtp_ssl=False
)

# Send email
yag.send(
    to=receiver_email,
    subject=subject,
    contents=message
)

print("Email sent successfully!")
