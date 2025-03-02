import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from tasks.file_conversion import convert_files
from db.database import tasks_collection

# Configure logging
logging.basicConfig(filename="logs/scheduler.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Global scheduler instance
scheduler = BackgroundScheduler()
scheduler.start()

def schedule_conversion(directory, ext, format, mode, interval=None, run_date=None, cron_time=None):
    """Schedule file conversion tasks."""
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

    except Exception as e:
        logging.error(f"Failed to schedule task: {e}")
