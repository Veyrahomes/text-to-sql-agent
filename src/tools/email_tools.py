"""Email delivery tools for the Text-to-SQL agent."""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


def send_email(
    to_email: str,
    subject: str,
    body: str,
    from_email: str = None,
    smtp_password: str = None,
) -> Dict[str, Any]:
    """Send an email with query results using Gmail SMTP."""
    from_email = from_email or os.getenv("EMAIL_ADDRESS", "wisdomcfriday1@gmail.com")
    smtp_password = smtp_password or os.getenv("EMAIL_APP_PASSWORD", "")

    if not smtp_password:
        return {
            "success": False,
            "error": "No email password configured. Set EMAIL_APP_PASSWORD in .env file."
        }

    try:
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        return {"success": True, "error": None}

    except Exception as e:
        return {"success": False, "error": str(e)}


def should_send_email(question: str) -> bool:
    """Check if user's question requests email delivery."""
    email_keywords = ["send", "email", "mail", "report", "deliver"]
    return any(kw in question.lower() for kw in email_keywords)