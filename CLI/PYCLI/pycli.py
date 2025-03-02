import argparse
import time
from scheduler.scheduler import schedule_conversion

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
        print("\n⏹ Scheduler stopped.")
