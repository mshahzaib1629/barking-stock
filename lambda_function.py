from app.app import App

def lambda_handler(event, context):
    app = App()
    app.get_announcements()
    announcements = app.announcements
    return announcements
