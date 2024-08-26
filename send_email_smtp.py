import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_template import get_email_body

# Configuration
port = 587
smtp_server = "live.smtp.mailtrap.io"
login = "api"  
password = "e48e3afd023334b8440e944a12a2856f"

sender_email = "Barking Stock <mailtrap@demomailtrap.com>"
receiver_email = "A Test User <mshahzaib1629@gmail.com>"

# Email content
subject = "HTML Email without Attachment"
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