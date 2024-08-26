import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_template import get_email_body
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration
port = os.getenv("SMTP_PORT")
smtp_server = os.getenv("SMTP_SERVER")
login = os.getenv('MAIL_TRAP_LOGIN') 
password = os.getenv("MAIL_TRAP_PASSWORD")
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = "Shahzaib <mshahzaib1629@gmail.com>"

# Email content
subject = f"Stock Announcement - {datetime.now().strftime('%Y-%m-%d %I:%M %p')}"
html = get_email_body()

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Attach the HTML part
message.attach(MIMEText(html, "html"))

# Send the email
with smtplib.SMTP(smtp_server, port) as server:
    server.starttls()
    server.login(login, password)
    server.sendmail(sender_email, receiver_email, message.as_string())

print('Sent')