import schedule
import time
from datetime import datetime
from database import get_scheduled_email_tasks, save_email_log
from tasks.email_automation import send_emails

def check_and_send_emails():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    email_tasks = get_scheduled_email_tasks()

    for task in email_tasks:
        if task["schedule_time"] == current_time:
            send_emails(task)
            task["sent"] = True
            save_email_log(task["emails"], task["subject"], task["message"], "sent")
            task.save()

# Schedule the job every minute
schedule.every().minute.at(":00").do(check_and_send_emails)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)