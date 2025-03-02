import os
import argparse
import time
import pandas as pd
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient, errors
import logging

# Configure logging
logging.basicConfig(filename="conversion.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logging.getLogger('apscheduler').setLevel(logging.DEBUG)  # Enable APScheduler logs

# Database setup
try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    db = client["file_conversion_db"]
    tasks_collection = db["tasks"]
    logs_collection = db["logs"]
    client.admin.command('ping')  # Check if MongoDB is reachable
except errors.ServerSelectionTimeoutError:
    logging.error("❌ MongoDB is not reachable. Exiting.")
    exit(1)

# Global scheduler instance
scheduler = BackgroundScheduler()
scheduler.start()

def log_task(directory, ext, format, status, message):
    """Log task details in the database and file."""
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
    except errors.PyMongoError as e:
        logging.error(f"Failed to log task in MongoDB: {e}")

def convert_files(directory, ext, format):
    """File conversion logic."""
    try:
        logging.info("Starting file conversion process")
        converted_files = []

        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")

        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)

            if os.path.isfile(file_path) and file.endswith(f".{ext}"):
                src = file_path
                dst = os.path.join(directory, file.replace(f".{ext}", f".{format}"))

                logging.info(f"Processing file: {src}")

                if not os.access(src, os.R_OK):
                    logging.error(f"Permission denied: {src}")
                    continue

                try:
                    df = pd.read_csv(src, delimiter="\t")  # Example for tab-separated text files
                    df.to_csv(dst, index=False)
                    converted_files.append(dst)
                    logging.info(f"Converted: {src} → {dst}")
                except Exception as file_error:
                    logging.error(f"Error converting {src}: {file_error}")

        log_task(directory, ext, format, "Success", f"Converted {len(converted_files)} files")
        logging.info("File conversion process completed")
    except Exception as e:
        log_task(directory, ext, format, "Failed", str(e))
        logging.error(f"Conversion failed: {e}")

def schedule_conversion(directory, ext, format, mode, interval=None, run_date=None, cron_time=None):
    """Schedule tasks in the background without blocking."""
    try:
        if mode == 'interval' and interval:
            job = scheduler.add_job(convert_files, 'interval', minutes=interval, args=[directory, ext, format])
        elif mode == 'cron' and cron_time:
            hour, minute = map(int, cron_time.split(':'))
            job = scheduler.add_job(convert_files, 'cron', hour=hour, minute=minute, args=[directory, ext, format])
        elif mode == 'date' and run_date:
            run_datetime = datetime.strptime(run_date, "%Y-%m-%d %H:%M:%S")
            job = scheduler.add_job(convert_files, 'date', run_date=run_datetime, args=[directory, ext, format])
        elif mode == "immediate":
            convert_files(directory, ext, format)
            exit(0)
        else:
            raise ValueError("Invalid scheduling parameters!")

        logging.info(f"Task scheduled with mode: {mode}")
        print(f"✅ Task scheduled successfully. Mode: {mode}")

        # Print and log scheduled jobs
        jobs = scheduler.get_jobs()
        print(f"🛠 Current scheduled jobs: {jobs}")
        logging.info(f"Current scheduled jobs: {jobs}")

        # Store scheduled task in database
        tasks_collection.insert_one({
            "directory": directory,
            "extension": ext,
            "format": format,
            "mode": mode,
            "interval": interval,
            "run_date": run_date,
            "cron_time": cron_time,
            "status": "Scheduled",
            "timestamp": datetime.now()
        })

    except errors.PyMongoError as e:
        logging.error(f"MongoDB error while scheduling task: {e}")
    except Exception as e:
        logging.error(f"Failed to schedule task: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Schedule file conversion tasks.")
    parser.add_argument("--dir", required=True, help="Directory containing files")
    parser.add_argument("--ext", required=True, help="File extension to convert")
    parser.add_argument("--format", required=True, help="Target file format")
    parser.add_argument("--mode", required=True, choices=["interval", "cron", "date", "immediate"], help="Scheduling mode")
    parser.add_argument("--interval", type=int, help="Interval time in minutes (for interval mode)")
    parser.add_argument("--run_date", help="Run date in YYYY-MM-DD HH:MM:SS format (for date mode)")
    parser.add_argument("--cron_time", help="Execution time in HH:MM format (for cron mode)")

    args = parser.parse_args()
    
    schedule_conversion(args.dir, args.ext, args.format, args.mode, args.interval, args.run_date, args.cron_time)

    # Keep script alive to allow scheduled jobs to execute
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
