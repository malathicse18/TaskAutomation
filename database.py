import pymongo
from datetime import datetime
from config import DB_CONNECTION_URL
import logging
import csv
from gridfs import GridFS

# Configure MongoDB connection
client = pymongo.MongoClient(DB_CONNECTION_URL)
db = client["TaskAutomation"]
fs = GridFS(db)

# Collections for each task
email_tasks_collection = db["email_tasks"]
email_logs_collection = db["email_logs"]
file_conversion_tasks_collection = db["file_conversion_tasks"]
log_compression_tasks_collection = db["log_compression_tasks"]
log_deletion_tasks_collection = db["log_deletion_tasks"]
web_scraping_tasks_collection = db["web_scraping_tasks"]
user_details_collection = db["user_details"]

# Ensure indexes for better performance
email_tasks_collection.create_index("schedule_time")
email_tasks_collection.create_index("emails.email", unique=True)
user_details_collection.create_index("email", unique=True)

def save_email_task(emails, subject, message, attachment=None, schedule_time=None, user_details=None):
    task_data = {
        "emails": emails,
        "subject": subject,
        "message": message,
        "attachment": attachment,
        "schedule_time": schedule_time,
        "user_details": user_details,
        "created_at": datetime.now()
    }
    try:
        email_tasks_collection.insert_one(task_data)
    except Exception as e:
        logging.error(f"Failed to save email task - Reason: {str(e)}")

def save_email_log(email, subject, message, status, error_message=None):
    log_data = {
        "email": email,
        "subject": subject,
        "message": message,
        "status": status,
        "error_message": error_message,
        "timestamp": datetime.now()
    }
    try:
        email_logs_collection.insert_one(log_data)
    except Exception as e:
        logging.error(f"Failed to save email log - Reason: {str(e)}")

def get_scheduled_email_tasks():
    return email_tasks_collection.find({"schedule_time": {"$ne": None}})

def save_user_details(user_id, name, email, preferences, csv_data=None):
    user_data = {
        "_id": user_id,
        "name": name,
        "email": email,
        "preferences": preferences,
        "csv_data": csv_data
    }
    try:
        user_details_collection.insert_one(user_data)
    except pymongo.errors.DuplicateKeyError:
        logging.error(f"User with email {email} already exists")
    except Exception as e:
        logging.error(f"Failed to save user details - Reason: {str(e)}")

def save_csv_data_to_db(csv_file_path, user_id):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        csv_data = list(reader)
        for row in csv_data:
            row['user_id'] = user_id
            try:
                email_tasks_collection.insert_one(row)
            except Exception as e:
                logging.error(f"Failed to save CSV data - Reason: {str(e)}")
        return csv_data

def save_csv_file_to_db(csv_file_path, user_id):
    with open(csv_file_path, 'rb') as file:
        try:
            fs.put(file, filename=f'{user_id}_emails.csv')
        except Exception as e:
            logging.error(f"Failed to save CSV file - Reason: {str(e)}")