import os
import argparse
import time
import threading
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient

# Database setup
client = MongoClient("mongodb://localhost:27017/")
db = client["file_conversion_db"]
tasks_collection = db["tasks"]
logs_collection = db["logs"]

def log_task(directory, ext, format, status, message):
    """Log task details in the database."""
    logs_collection.insert_one({
        "directory": directory,
        "extension": ext,
        "format": format,
        "status": status,
        "message": message,
        "timestamp": datetime.now()
    })

def convert_files(directory, ext, format):
    """Function to simulate file conversion."""
    try:
        print(f"Converting all {ext} files in {directory} to {format} at {datetime.now()}...")
        time.sleep(2)  # Simulated processing delay
        log_task(directory, ext, format, "Success", "Conversion complete")
        print("Conversion complete!")
    except Exception as e:
        log_task(directory, ext, format, "Failed", str(e))
        print(f"Conversion failed: {e}")

def schedule_conversion(directory, ext, format, mode, interval=None, run_date=None, cron_time=None):
    scheduler = BackgroundScheduler()
    
    if mode == 'interval':
        scheduler.add_job(convert_files, 'interval', minutes=interval, args=[directory, ext, format])
    elif mode == 'cron':
        hour, minute = map(int, cron_time.split(':'))
        scheduler.add_job(convert_files, 'cron', hour=hour, minute=minute, args=[directory, ext, format])
    elif mode == 'date':
        scheduler.add_job(convert_files, 'date', run_date=run_date, args=[directory, ext, format])
    else:
        print("Invalid scheduling mode!")
        return
    
    scheduler.start()
    print("Scheduler started in the background.")

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

    # Run the scheduler in a separate daemon thread (so the main script exits cleanly)
    thread = threading.Thread(target=lambda: time.sleep(999999), daemon=True)
    thread.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Schedule file conversion tasks.")
    parser.add_argument("--dir", required=True, help="Directory containing files")
    parser.add_argument("--ext", required=True, help="File extension to convert")
    parser.add_argument("--format", required=True, help="Target file format")
    parser.add_argument("--mode", required=True, choices=["interval", "cron", "date"], help="Scheduling mode")
    parser.add_argument("--interval", type=int, help="Interval time in minutes (for interval mode)")
    parser.add_argument("--run_date", help="Run date in YYYY-MM-DD HH:MM:SS format (for date mode)")
    parser.add_argument("--cron_time", help="Execution time in HH:MM format (for cron mode)")
    
    args = parser.parse_args()
    schedule_conversion(args.dir, args.ext, args.format, args.mode, args.interval, args.run_date, args.cron_time)

    print("Main script exiting, but the scheduler is running in the background.")
