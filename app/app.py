from app.utils.psx_announcements import scrap_psx_company_announcement_page
from app.utils.send_email import SendEmail
from app.utils.firebase import initialize_firebase
from app.utils.user_stock_mapping import get_firebase_filtered_users, get_user_announcements
from dotenv import load_dotenv
load_dotenv()

class App:
    announcements = []
    users = []
    fetch_date_time_epoch = None
    variables_ref = None
    
    def __init__(self) -> None:
        self.app, self.db = initialize_firebase()
        
    def _update_last_fetched_epoch(self):
        self.variables_ref.update({'lastFetchTimeEpoch': self.fetch_date_time_epoch})
    
    def get_announcements(self):
            self.fetch_date_time_epoch, all_announcements = scrap_psx_company_announcement_page()
            
            # shortlist new announcements with the help of lastFetchTime
            self.variables_ref = self.db.collection("metaData").document("variables")
            variables = self.variables_ref.get().to_dict()
            last_fetch_time_epoch = variables['lastFetchTimeEpoch']
            
            self.announcements = [announcement for announcement in all_announcements if announcement["EPOCH"] > last_fetch_time_epoch]
            
            # we are updating the last fetch time in firebase after sending emails, so that if a job fails, the announcements can be fetched in succeeding job
            # self._update_last_fetched_epoch()

    def get_filtered_users(self):
        stock_symbols = [stock['SYMBOL'] for stock in self.announcements]
        self.users = get_firebase_filtered_users(self.db.collection("users"), stock_symbols)
        self.users = get_user_announcements(self.users, self.announcements)

        
    def send_email_announcements(self):
        for user_announcement in self.users:
            if len(user_announcement['relevantAnnouncements']) > 0:
                
                announcements_symbols = set([announcement['SYMBOL'] for announcement in user_announcement['relevantAnnouncements']])

                email_subject = "Stock Announcements - " + ", ".join(announcements_symbols)

                email_sender = SendEmail()
                email_sender.notify_stock_announcements(user_announcement, email_subject)
                
        self._update_last_fetched_epoch()