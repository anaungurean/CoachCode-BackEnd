import psycopg2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
from passlib.hash import bcrypt_sha256
from datetime import datetime
import config


def generate_reset_code(length=6):
    characters = string.ascii_letters + string.digits
    reset_code = ''.join(random.choice(characters) for i in range(length))
    return reset_code


def send_email(to_email, subject, message):
    global server
    try:
        server = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
        server.ehlo()
        email = config.EMAIL
        password = config.PASSWORD

        server.login(email, password)

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        server.sendmail(email, to_email, msg.as_string())
        return True
    except Exception as e:
        print("Failed to send email. Error:", e)
        return False
    finally:
        server.quit()


