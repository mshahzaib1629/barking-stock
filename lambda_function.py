from psx_announcements import scrap_psx_company_announcement_page

def lambda_handler(event, context):
    announcements = scrap_psx_company_announcement_page()
    return announcements
