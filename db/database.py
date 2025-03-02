from pymongo import MongoClient, errors
import logging

# Configure logging
logging.basicConfig(filename="logs/db.log", level=logging.DEBUG,
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
