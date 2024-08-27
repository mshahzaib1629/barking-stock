from app.utils.psx_announcements import scrap_psx_company_announcement_page
from app.utils.send_email import SendEmail
from app.utils.firebase import initialize_firebase
from app.utils.user_stock_mapping import get_firebase_filtered_users, get_user_announcements
from dotenv import load_dotenv
load_dotenv()

class App:
    announcements = []
    users = []
    
    def __init__(self) -> None:
        self.app, self.db = initialize_firebase()
    
    def get_announcements(self):
            fetch_date_time_epoch, all_announcements = scrap_psx_company_announcement_page()
            
            # shortlist new announcements with the help of lastFetchTime
            variables_ref = self.db.collection("metaData").document("variables")
            variables = variables_ref.get().to_dict()
            last_fetch_time_epoch = variables['lastFetchTimeEpoch']
            
            self.announcements = [announcement for announcement in all_announcements if announcement["EPOCH"] > last_fetch_time_epoch]
            
            variables_ref.update({'lastFetchTimeEpoch': fetch_date_time_epoch})
            

    def get_filtered_users(self):
        stock_symbols = [stock['SYMBOL'] for stock in self.announcements]
        self.users = get_firebase_filtered_users(self.db.collection("users"), stock_symbols)
        self.users = get_user_announcements(self.users, self.announcements)

        
    def send_email_announcements(self):
        for user_announcement in self.users:
            if len(user_announcement['relevantAnnouncements']) > 0:
                
                announcements_symbols = [announcement['SYMBOL'] for announcement in user_announcement['relevantAnnouncements']]
                email_subject = "Stock Announcements - " + ", ".join(announcements_symbols)

                email_sender = SendEmail()
                email_sender.notify_stock_announcements(user_announcement, email_subject)