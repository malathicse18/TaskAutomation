import pymongo
import logging
import csv
import uuid
from datetime import datetime
from config import DB_CONNECTION_URL  # Ensure this points to your MongoDB connection string
from gridfs import GridFS

# Configure MongoDB connection
client = pymongo.MongoClient(DB_CONNECTION_URL)
db = client["TaskAutomation"]  # Your database name
fs = GridFS(db)

# Collections
email_tasks_collection = db["email_tasks"]
email_logs_collection = db["email_logs"]
file_conversion_tasks_collection = db["file_conversion_tasks"]
log_compression_tasks_collection = db["log_compression_tasks"]
log_deletion_tasks_collection = db["log_deletion_tasks"]
web_scraping_tasks_collection = db["web_scraping_tasks"]
gold_rates_collection = db["gold_rates"]

# Create indexes safely
def create_index_safe(collection, keys, **kwargs):
    """Creates an index safely without duplicate conflicts."""
    existing_indexes = collection.index_information()
    index_key = tuple(keys) if isinstance(keys, list) else (keys,)

    for index in existing_indexes.values():
        if index.get("key") == list(index_key):
            logging.info(f"Index {index_key} already exists in {collection.name}. Skipping...")
            return

    try:
        collection.create_index(keys, **kwargs)
        logging.info(f"Created index {index_key} on {collection.name}")
    except pymongo.errors.PyMongoError as e:
        logging.error(f"Error creating index {index_key} - {e}")

# Apply indexes
create_index_safe(email_tasks_collection, "schedule_time")
create_index_safe(email_tasks_collection, [("emails.email", pymongo.ASCENDING)], unique=True, sparse=True)
create_index_safe(gold_rates_collection, "date", unique=True)

# Function to save email task
def save_email_task(emails, subject, message, attachment=None, schedule_hour=None, schedule_minute=None, frequency=None, user_details=None):
    task_data = {
        "_id": str(uuid.uuid4()),
        "user_id": user_details["user_id"],
        "name": user_details["name"],
        "email": user_details["email"],
        "csv_data": emails,
        "subject": subject,
        "message": message,
        "attachment": attachment,
        "schedule_hour": schedule_hour,
        "schedule_minute": schedule_minute,
        "frequency": frequency,
        "created_at": datetime.now()
    }
    try:
        email_tasks_collection.insert_one(task_data)
        logging.info(f"Email task saved successfully for user: {user_details['email']}")
    except pymongo.errors.DuplicateKeyError:
        logging.error("Duplicate email entry detected. Skipping task.")
    except pymongo.errors.PyMongoError as e:
        logging.error(f"Failed to save email task - Reason: {e}")

# Function to log email sending results
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
        logging.info(f"Email log saved for: {email}, Status: {status}")
    except pymongo.errors.PyMongoError as e:
        logging.error(f"Failed to save email log - Reason: {e}")

# Fetch scheduled email tasks safely
def get_scheduled_email_tasks():
    try:
        return email_tasks_collection.find(
            {"schedule_hour": {"$ne": None}, "schedule_minute": {"$ne": None}, "frequency": {"$ne": None}}
        )
    except pymongo.errors.PyMongoError as e:
        logging.error(f"Error fetching scheduled email tasks: {e}")
        return []

# Save user details inside task
def save_user_details_in_task(user_id, name, email, preferences, csv_data=None):
    return {
        "user_id": user_id,
        "name": name,
        "email": email,
        "preferences": preferences,
        "csv_data": csv_data
    }

# Store CSV file contents in DB
def save_csv_data_to_db(csv_file_path, user_id):
    try:
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_data = [{"email": row["email"]} for row in reader]
        return csv_data
    except Exception as e:
        logging.error(f"Error reading CSV file {csv_file_path}: {e}")
        return []

# Save CSV file as GridFS in MongoDB
def save_csv_file_to_db(csv_file_path, user_id):
    try:
        with open(csv_file_path, 'rb') as file:
            fs.put(file, filename=f'{user_id}_emails.csv')
        logging.info(f"CSV file stored in MongoDB for user: {user_id}")
    except pymongo.errors.PyMongoError as e:
        logging.error(f"Failed to save CSV file - Reason: {e}")

# Save web scraping results
def save_web_scraping_task(url, scraped_data, user_details):
    task_data = {
        "_id": str(uuid.uuid4()),
        "user_id": user_details["user_id"],
        "url": url,
        "scraped_data": scraped_data,
        "created_at": datetime.now()
    }
    try:
        web_scraping_tasks_collection.insert_one(task_data)
        logging.info(f"Web scraping task saved successfully for URL: {url}")
    except pymongo.errors.PyMongoError as e:
        logging.error(f"Failed to save web scraping task - Reason: {e}")

# Store gold rate data with optimized update logic
def store_gold_rate(data):
    try:
        logging.info(f"Storing gold rate data: {data}")
        gold_rates_collection.update_one(
            {"date": data['date']},
            {"$set": {"24K": data['24K'], "22K": data['22K']}},
            upsert=True
        )
        logging.info("Gold rate data stored successfully.")
    except pymongo.errors.PyMongoError as e:
        logging.error(f"MongoDB error storing gold rate: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error storing gold rate data: {e}")
        raise
