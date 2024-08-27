import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.utils.email_templates.stock_announcements import stock_announcement_body
from datetime import datetime
import os

class SendEmail:
    
    def __init__(self) -> None:
        self.port = os.getenv("SMTP_PORT")
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.login = os.getenv('MAIL_TRAP_LOGIN') 
        self.password = os.getenv("MAIL_TRAP_PASSWORD")
        self.sender_email = os.getenv("SENDER_EMAIL")
        

    def notify_stock_announcements(self, receiver_data, announcements=[], subject=None):      
        receiver_email = receiver_data["email"]
        data = {
            "recipient_name": receiver_data["name"],
            "announcements": announcements
        }
        
        if subject is None:
            subject = f"Stock Announcements - {datetime.now().strftime('%Y-%m-%d %I:%M %p')}"
        
        # Email content
        html = stock_announcement_body(data)

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Attach the HTML part
        message.attach(MIMEText(html, "html"))

        # Send the email
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls()
            server.login(self.login, self.password)
            server.sendmail(self.sender_email, receiver_email, message.as_string())

        print(f'Email sent to {receiver_email}')