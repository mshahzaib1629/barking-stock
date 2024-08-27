import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.utils.email_templates.stock_announcements import stock_announcement_body
from datetime import datetime
import os
# Sample data to populate the template
data = {
        "recipient_name": "Shahzaib",
    "announcements": [
        {
            "stock_name": "Apple Inc.",
            "symbol": "AAPL",
            "logo_url": "https://pngimg.com/d/apple_logo_PNG19666.png",
            "title": "Q3 Earnings Report",
            "attachment_links": [
                {"name": "Q3 Earnings Report PDF", "url": "https://example.com/aapl_q3_report.pdf"},
                {"name": "Investor Presentation", "url": "https://example.com/aapl_investor_presentation.pdf"}
            ]
        },
        {
            "stock_name": "Tesla Inc.",
            "symbol": "TSLA",
            "logo_url": "https://pngimg.com/uploads/tesla_logo/tesla_logo_PNG19.png",
            "title": "New Model Launch Event",
            "attachment_links": [
                {"name": "Event Details PDF", "url": "https://example.com/tsla_event_details.pdf"}
            ]
        },
        {
            "stock_name": "Amazon.com Inc.",
            "symbol": "AMZN",
            "logo_url": "https://pngimg.com/d/amazon_PNG15.png",
            "title": "Strategic Partnership Announcement",
            "attachment_links": [
                {"name": "Partnership Details PDF", "url": "https://example.com/amzn_partnership.pdf"},
                {"name": "Press Release", "url": "https://example.com/amzn_press_release.pdf"}
            ]
        },
        {
            "stock_name": "Microsoft Corp.",
            "symbol": "MSFT",
            "logo_url": "https://cdn-icons-png.flaticon.com/512/732/732221.png",
            "title": "Upcoming Product Updates",
            "attachment_links": [
                {"name": "Product Roadmap PDF", "url": "https://example.com/msft_product_roadmap.pdf"}
            ]
        },
        {
            "stock_name": "Alphabet Inc.",
            "symbol": "GOOGL",
            "logo_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6HMrE7xvKu5-UahOPBs3GcE4AZJk8LsX7tg&s",
            "title": "Annual Shareholder Meeting Agenda",
            "attachment_links": [
                {"name": "Agenda PDF", "url": "https://example.com/googl_agenda.pdf"},
                {"name": "Meeting Details", "url": "https://example.com/googl_meeting_details.pdf"}
            ]
        },
    ],
    "sender_name": "Alice Smith",
    "sender_position": "Financial Analyst",
    "sender_company": "XYZ Investments"
}

class SendEmail:
    
    def __init__(self) -> None:
        self.port = os.getenv("SMTP_PORT")
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.login = os.getenv('MAIL_TRAP_LOGIN') 
        self.password = os.getenv("MAIL_TRAP_PASSWORD")
        self.sender_email = os.getenv("SENDER_EMAIL")
        

    def notify_stock_announcements(self, receiver_data, announcements=[], subject=None):      
        receiver_email = receiver_data["email"]
        receiver_name = receiver_data["name"]
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