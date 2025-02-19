from apscheduler.schedulers.blocking import BlockingScheduler
import logging
from pytz import timezone
from tasks.email_automation import send_emails
from database import get_scheduled_email_tasks

# Set up logging
logging.basicConfig(filename='scheduler.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
print("Starting scheduler...")

def schedule_email_automation():
    """Runs the email automation task."""
    logger.info("Email automation task started")
    print("Email automation task started")
    try:
        tasks = get_scheduled_email_tasks()
        task_count = 0
        for task in tasks:
            send_emails(task)
            task_count += 1
        logger.info(f"Email automation task completed. Processed {task_count} tasks.")
        print(f"Email automation task completed. Processed {task_count} tasks.")
    except Exception as e:
        logger.error(f"Error in email automation task: {str(e)}")
        print(f"Error in email automation task: {str(e)}")

def get_schedule_details():
    """Fetches the scheduling details from the database."""
    tasks = get_scheduled_email_tasks()
    if tasks and len(tasks) > 0:
        task = tasks[0]  # Get the first scheduled task
        logger.info(f"Found scheduled task: {task}")
        print(f"Found scheduled task: {task}")
        return task['schedule_hour'], task['schedule_minute'], task['frequency']
    else:
        logger.error("No scheduled email tasks found in the database.")
        print("No scheduled email tasks found in the database.")
        return None, None, None

scheduler = BlockingScheduler()

# Fetch scheduling details from the database
hour, minute, frequency = get_schedule_details()
print(f"Scheduling details - Hour: {hour}, Minute: {minute}, Frequency: {frequency}")

if hour is not None and minute is not None and frequency is not None:
    # Set the job based on the fetched scheduling details
    if frequency == 'daily':
        logger.info(f"Scheduling daily email automation at {hour}:{minute}")
        print(f"Scheduling daily email automation at {hour}:{minute}")
        scheduler.add_job(schedule_email_automation, 'cron', hour=hour, minute=minute, timezone=timezone('Asia/Kolkata'))
    elif frequency == 'weekly':
        logger.info(f"Scheduling weekly email automation at {hour}:{minute}")
        print(f"Scheduling weekly email automation at {hour}:{minute}")
        scheduler.add_job(schedule_email_automation, 'cron', day_of_week='mon', hour=hour, minute=minute, timezone=timezone('Asia/Kolkata'))
    else:
        logger.error(f"Unsupported frequency: {frequency}")
        print(f"Unsupported frequency: {frequency}")

    print("Scheduler started...")
    scheduler.start()
else:
    logger.error("Failed to schedule email automation due to missing scheduling details.")
    print("Failed to schedule email automation due to missing scheduling details.")
