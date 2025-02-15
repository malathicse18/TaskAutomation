# import pymongo
# from datetime import datetime
# from config import DB_CONNECTION_URL

# # Configure MongoDB connection
# client = pymongo.MongoClient(DB_CONNECTION_URL)
# db = client["email_automation"]
# email_tasks_collection = db["email_tasks"]
# email_logs_collection = db["email_logs"]

# def save_email_task(emails, subject, message, attachment=None, schedule_time=None, user_details=None):
#     task_data = {
#         "emails": emails,
#         "subject": subject,
#         "message": message,
#         "attachment": attachment,
#         "schedule_time": schedule_time,
#         "user_details": user_details,
#         "created_at": datetime.now()
#     }
#     email_tasks_collection.insert_one(task_data)

# def save_email_log(email, subject, message, status, error_message=None):
#     log_data = {
#         "email": email,
#         "subject": subject,
#         "message": message,
#         "status": status,
#         "error_message": error_message,
#         "timestamp": datetime.now()
#     }
#     email_logs_collection.insert_one(log_data)

# def get_scheduled_email_tasks():
#     return email_tasks_collection.find({"schedule_time": {"$ne": None}})
import pymongo
from datetime import datetime
from config import DB_CONNECTION_URL

# Configure MongoDB connection
client = pymongo.MongoClient(DB_CONNECTION_URL)
db = client["email_automation_db"]
emails_collection = db["emails"]
tasks_collection = db["tasks"]
users_collection = db["users"]

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
    tasks_collection.insert_one(task_data)

def save_email_log(email, subject, message, status, error_message=None):
    log_data = {
        "email": email,
        "subject": subject,
        "message": message,
        "status": status,
        "error_message": error_message,
        "timestamp": datetime.now()
    }
    emails_collection.insert_one(log_data)

def get_scheduled_email_tasks():
    return tasks_collection.find({"schedule_time": {"$ne": None}})

def save_user_details(user_id, name, email, preferences):
    user_data = {
        "_id": user_id,
        "name": name,
        "email": email,
        "preferences": preferences
    }
    users_collection.insert_one(user_data)