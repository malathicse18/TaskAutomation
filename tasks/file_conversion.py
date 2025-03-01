import os
import argparse
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time

def convert_files(directory, ext, format):
    """Function to simulate file conversion."""
    print(f"Converting all {ext} files in {directory} to {format} at {datetime.now()}...")
    # Simulated processing delay
    time.sleep(2)
    print("Conversion complete!")

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
    print("Scheduler started. Press Ctrl+C to exit.")
    
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped.")

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
