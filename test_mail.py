import smtplib, ssl
from email.message import EmailMessage
port = 587
smtp_server = "smtp.zeptomail.in"
username="emailapikey"
password = "Zoho-enczapikey PHtE6r1ZReHjjGUq+kNT5P+4FZKlYN8p/uNlKQAT5Y5LCPIGH00BqNB9kTHjohgiVfdBHPLNnNpgsLmVuu+HIj2+YzxFCGqyqK3sx/VYSPOZsbq6x00at14SfkzYUoXtddVj3SDWvtbSNA=="
message = "Test email sent successfully."
msg = EmailMessage()
msg['Subject'] = "Test Email"
msg['From'] = "alerts@getnotify.in"
msg['To'] = "prathmeshpatiltoi@gmail.com"
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
        print ("use 465 / 587 as port value")
        exit()
    print ("successfully sent")
except Exception as e:
    print (e)