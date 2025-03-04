import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from tasks.file_conversion import convert_files
from db.database import get_db
import os

# Ensure logs directory exists
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs"))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logging to use db.log
log_file = os.path.join(log_dir, "db.log")
logging.basicConfig(filename=log_file, level=logging.DEBUG,  # Set to DEBUG for troubleshooting
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Global scheduler instance
scheduler = BackgroundScheduler()
scheduler.start()

def schedule_conversion(directory, ext, format, mode, interval=None, run_date=None, cron_time=None):
    """Schedule file conversion tasks."""
    try:
        if mode == 'interval' and interval:
            job = scheduler.add_job(convert_files, 'interval', minutes=interval, args=[directory, ext, format])
            print(f"Scheduled interval job: {job}")
            logging.debug(f"Scheduled interval job: {job}")
        elif mode == 'cron' and cron_time:
            hour, minute = map(int, cron_time.split(':'))
            job = scheduler.add_job(convert_files, 'cron', hour=hour, minute=minute, args=[directory, ext, format])
            print(f"Scheduled cron job: {job}")
            logging.debug(f"Scheduled cron job: {job}")
        elif mode == 'date' and run_date:
            run_datetime = datetime.strptime(run_date, "%Y-%m-%d %H:%M:%S")
            job = scheduler.add_job(convert_files, 'date', run_date=run_datetime, args=[directory, ext, format])
            print(f"Scheduled date job: {job}")
            logging.debug(f"Scheduled date job: {job}")
        elif mode == "immediate":
            convert_files(directory, ext, format)
            print("Immediate conversion executed")
            logging.debug("Immediate conversion executed")
            exit(0)
        else:
            raise ValueError("Invalid scheduling parameters!")
        print("Scheduled Jobs:", scheduler.get_jobs())
        logging.info(f"Scheduled Jobs: {scheduler.get_jobs()}")

        logging.info(f"Task scheduled with mode: {mode}")
        print(f"✅ Task scheduled successfully. Mode: {mode}")

        # Store scheduled task in database
        client, db = get_db()
        tasks_collection = db["tasks"]
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
        client.close()

    except Exception as e:
        logging.error(f"Failed to schedule task: {e}")

if __name__ == "__main__":
    import time
    while True:
        time.sleep(1)