from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
from email_automation import send_emails

def schedule_emails(args):
    scheduler = BackgroundScheduler()
    schedule_time = datetime.strptime(args.schedule, "%H:%M").time()

    def job():
        task = {
            "emails": args.emails,
            "subject": args.subject,
            "message": args.message,
            "attachment": args.attachment,
            "schedule_time": args.schedule
        }
        send_emails(task)

    scheduler.add_job(job, 'cron', hour=schedule_time.hour, minute=schedule_time.minute)
    scheduler.start()

    print(f"Scheduling email automation at {args.schedule}...")

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == "__main__":
    # Example usage
    class Args:
        emails = ["example@example.com"]
        subject = "Test Email"
        message = "Hello!"
        attachment = None
        schedule = "21:17"

    schedule_emails(Args())