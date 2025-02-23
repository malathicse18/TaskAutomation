import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SMTP_USER = os.getenv('EMAIL_SENDER')
SMTP_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
RECIPIENTS_CSV_PATH = os.getenv('RECIPIENTS_CSV_PATH')
MONGO_URI = os.getenv('MONGO_URI')
DB_CONNECTION_URL = os.getenv('DB_CONNECTION_URL')