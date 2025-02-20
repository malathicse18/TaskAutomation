import csv
import logging
import os
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from config import RECIPIENTS_CSV_PATH, SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

logging.basicConfig(filename='email_automation.log', level=logging.INFO)

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def read_recipients_from_csv(file_path):
    valid_recipients = []
    invalid_recipients = []
    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                email = row[0].strip()
                if is_valid_email(email):
                    valid_recipients.append(email)
                else:
                    invalid_recipients.append(email)
                    logging.warning(f"Invalid email address found: {email}")
    except FileNotFoundError:
        logging.error(f"CSV file not found: {file_path}")
    return valid_recipients, invalid_recipients

def create_email(recipient_email, user_data):
    email_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email Template</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
            }}
            .container {{
                width: 80%;
                margin: auto;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f9f9f9;
            }}
            .header {{
                text-align: center;
                padding-bottom: 20px;
            }}
            .content {{
                margin-bottom: 20px;
            }}
            .footer {{
                text-align: center;
                font-size: 0.9em;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Hello, {name}!</h1>
            </div>
            <div class="content">
                <p>{message}</p>
            </div>
            <div class="footer">
                <p>Best regards,<br>Your Company</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        email_content = email_template.format(name=user_data['name'], message=user_data['message'])
    except KeyError as e:
        logging.error(f"Missing key in user data for template: {e}")
        return None

    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = recipient_email
    msg['Subject'] = user_data['subject']
    msg.attach(MIMEText(email_content, 'html'))
    return msg

def send_email(msg):
    try:
        with SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            logging.info(f"Email sent to {msg['To']}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def process_email_task(user_data):
    valid_recipients, invalid_recipients = read_recipients_from_csv(RECIPIENTS_CSV_PATH)
    if invalid_recipients:
        logging.warning(f"Invalid email addresses found: {', '.join(invalid_recipients)}")
        print(f"Invalid email addresses found: {', '.join(invalid_recipients)}")
    
    if not valid_recipients:
        logging.error("No valid email addresses found. Aborting email sending.")
        print("No valid email addresses found. Aborting email sending.")
        return
    
    for recipient in valid_recipients:
        msg = create_email(recipient, user_data)
        if msg:
            send_email(msg)