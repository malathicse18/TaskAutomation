from dotenv import load_dotenv
import os

load_dotenv()

DB_CONNECTION_URL = os.getenv("DB_CONNECTION_URL")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))