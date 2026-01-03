from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
TEST_RECIPIENT = os.getenv("TEST_RECIPIENT")

def send_email(content: str):
    """Send an email with the given content."""

    SUBJECT = "Grocery Compiler Results"

    message = Mail(
        from_email=TEST_RECIPIENT,
        to_emails=TEST_RECIPIENT,
        subject=SUBJECT,
        plain_text_content=content
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Status: {response.status_code}")
        print(f"Body: {response.body}")
        print(f"Headers: {response.headers}")
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, 'body'):
            print(f"Error details: {e.body}")
