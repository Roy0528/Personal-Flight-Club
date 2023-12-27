import os
import smtplib, ssl
from email.mime.text import MIMEText

USERNAME = "roy32011@gmail.com"
HOST = "smtp.gmail.com"
PORT = 465
PASSWORD = os.getenv("PASSWORD")


class EmailManager:
    def send_email(self, receiver_email, subject, message):
        receiver = receiver_email
        context = ssl.create_default_context()

        html_message = MIMEText(message, "html")
        html_message["Subject"] = subject
        html_message["From"] = USERNAME
        html_message["To"] = receiver_email

        with smtplib.SMTP_SSL(HOST, PORT, context=context) as server:
            server.login(USERNAME, PASSWORD)
            server.sendmail(USERNAME, receiver, html_message.as_string())
