from pymongo import MongoClient, errors
import logging
import os

# Ensure logs directory exists
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs"))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logging
log_file = os.path.join(log_dir, "db.log")
logging.basicConfig(filename=log_file, level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def get_db():
    """Connect to MongoDB and return the database instance."""
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        db = client["file_conversion_db"]
        client.admin.command('ping')  # Check if MongoDB is reachable
        logging.info("✅ Connected to MongoDB")
        return db
    except errors.ServerSelectionTimeoutError:
        logging.error("❌ MongoDB is not reachable. Exiting.")
        exit(1)

# Collections
db = get_db()
tasks_collection = db["tasks"]
logs_collection = db["logs"]
