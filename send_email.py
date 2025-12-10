# send_email.py — debug-friendly
import os
import traceback
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main():
    # Read API key from env
    key = os.environ.get("SENDGRID_API_KEY")
    print("DEBUG: SENDGRID_API_KEY found?" , "YES" if key else "NO")

    FROM = "prathmeshpatiltoi@gmail.com"   # your verified single-sender
    TO = "prathmeshpatiltoi@gmail.com"     # test sending to yourself

    if not key:
        print("ERROR: SENDGRID_API_KEY environment variable is not set.")
        print("If you are using PowerShell, run:")
        print(r'$env:SENDGRID_API_KEY = "SG.xxxxx-your-key-xxxxx"')
        return

    message = Mail(
        from_email=FROM,
        to_emails=TO,
        subject="GETNOTIFY — test email",
        html_content="<strong>Hello from GETNOTIFY — test</strong>"
    )

    try:
        sg = SendGridAPIClient(key)
        print("DEBUG: Sending email now...")
        response = sg.send(message)
        print("DEBUG: SendGrid response status:", response.status_code)
        # response.body might be bytes; attempt decode
        try:
            body = response.body.decode() if hasattr(response.body, "decode") else response.body
        except Exception:
            body = response.body
        print("DEBUG: SendGrid response body:", body)
        print("DEBUG: SendGrid response headers:", response.headers)
        if response.status_code == 202:
            print("SUCCESS: Email accepted by SendGrid (202). Check inbox/spam.")
        else:
            print("WARNING: Non-202 status — check response above.")
    except Exception as e:
        print("EXCEPTION while sending:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
