from app.utils.psx_announcements import scrap_psx_company_announcement_page
from app.utils.send_email import SendEmail
from dotenv import load_dotenv
load_dotenv()

class App:
    announcements = []
    
    def __init__(self) -> None:
        pass
    
    def get_announcements(self):
            self.announcements = scrap_psx_company_announcement_page()

    def send_email_announcements(self):
        receiver_data = {
            "email": "mshahzaib1629@gmail.com",
            "name": ""
        }
        email_sender = SendEmail()
        email_sender.notify_stock_announcements(receiver_data, self.announcements)