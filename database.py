import pymongo
from datetime import datetime
from config import DB_CONNECTION_URL  # Make sure this points to your MongoDB connection string
import logging
import csv
from gridfs import GridFS
import uuid

# Configure MongoDB connection
client = pymongo.MongoClient(DB_CONNECTION_URL)
db = client["TaskAutomation"]  # Your database name
fs = GridFS(db)

# Collections for each task
email_tasks_collection = db["email_tasks"]
email_logs_collection = db["email_logs"]
file_conversion_tasks_collection = db["file_conversion_tasks"]
log_compression_tasks_collection = db["log_compression_tasks"]
log_deletion_tasks_collection = db["log_deletion_tasks"]
web_scraping_tasks_collection = db["web_scraping_tasks"]
gold_rates_collection = db["gold_rates"]  # Collection for gold rates

# Ensure indexes for better performance (add more as needed)
email_tasks_collection.create_index("schedule_time")
email_tasks_collection.create_index("emails.email", unique=True)
gold_rates_collection.create_index("date", unique=True)  # Index for gold rates date

def save_email_task(emails, subject, message, attachment=None, schedule_time=None, user_details=None):
    task_data = {
        "user_id": user_details["user_id"],
        "name": user_details["name"],
        "email": user_details["email"],
        "csv_data": emails,
        "subject": subject,
        "message": message,
        "attachment": attachment,
        "schedule_time": schedule_time,
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

def save_user_details_in_task(user_id, name, email, preferences, csv_data=None):
    user_data = {
        "user_id": user_id,
        "name": name,
        "email": email,
        "preferences": preferences,
        "csv_data": csv_data
    }
    return user_data

def save_csv_data_to_db(csv_file_path, user_id):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        csv_data = [{"email": row["email"]} for row in reader]  # Adapt if your CSV has more columns
        return csv_data

def save_csv_file_to_db(csv_file_path, user_id):
    with open(csv_file_path, 'rb') as file:
        try:
            fs.put(file, filename=f'{user_id}_emails.csv')
        except Exception as e:
            logging.error(f"Failed to save CSV file - Reason: {str(e)}")

def save_web_scraping_task(url, scraped_data, user_details):
    task_data = {
        "user_id": user_details["user_id"],
        "url": url,
        "scraped_data": scraped_data,
        "created_at": datetime.now()
    }
    try:
        web_scraping_tasks_collection.insert_one(task_data)
    except Exception as e:
        logging.error(f"Failed to save web scraping task - Reason: {str(e)}")

def store_gold_rate(data):
    try:
        # Check for existing record (using date as primary key)
        print(f"Storing data: {data}")  # Add this line to check the data being stored
        existing_record = gold_rates_collection.find_one({"date": data['date']})

        if existing_record:
            print("Updating existing record")  # Add this line
            gold_rates_collection.update_one(
                {"date": data['date']},
                {"$set": {"24K": data['24K'], "22K": data['22K']}}
            )
        else:
            print("Inserting new record")  # Add this line
            gold_rates_collection.insert_one(data)

    except pymongo.errors.PyMongoError as e:  # Catch MongoDB specific errors
        logging.error(f"MongoDB error storing gold rate: {e}")
        raise  # Re-raise to handle it in cli.py
    except Exception as e:
        logging.error(f"An unexpected error occurred while storing gold rate data: {e}")
        raise  # Re-raise to handle it in cli.py