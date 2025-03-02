import logging
from datetime import datetime
from db.database import logs_collection

# Configure logging
logging.basicConfig(filename="logs/conversion.log", level=logging.DEBUG,
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
        logs_collection.insert_one(log_entry)
        logging.info(f"Task Log: {log_entry}")
    except Exception as e:
        logging.error(f"Failed to log task in MongoDB: {e}")
