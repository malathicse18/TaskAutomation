import logging
from datetime import datetime
from db.database import get_db
import os

# Ensure logs directory exists
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs"))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logging
log_file = os.path.join(log_dir, "conversion.log")
logging.basicConfig(filename=log_file, level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def log_task(directory, ext, format, status, message):
    """Log task details in MongoDB and file."""
    log_entry = {
        "directory": directory,
        "extension": ext,
        "format": format,
        "status": status,
        "message": message,
        "timestamp": datetime.now()
    }
    try:
        client, db = get_db()
        logs_collection = db["logs"]
        logs_collection.insert_one(log_entry)
        client.close()
        logging.info(f"Task Log: {log_entry}")
    except Exception as e:
        logging.error(f"Failed to log task in MongoDB: {e}")