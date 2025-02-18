from apscheduler.schedulers.blocking import BlockingScheduler
import uuid
import logging
from pytz import timezone
from tasks.email_automation import email_automation
from config import EMAIL_SENDER
from database import save_csv_data_to_db, save_user_details_in_task, save_email_task

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def schedule_email_automation():
    logger.info("Email automation task started")
    args = {
        'file': 'emails.csv',
        'subject': 'Test Email',
        'message': 'Hello!',
        'user_name': 'John Doe',
        'user_email': EMAIL_SENDER
    }
    user_id = f"{args['user_email']}_{uuid.uuid4()}"
    csv_data = save_csv_data_to_db(args['file'], user_id)
    user_details = save_user_details_in_task(
        user_id=user_id, name=args['user_name'], email=EMAIL_SENDER, preferences={}, csv_data=csv_data
    )
    save_email_task(emails=csv_data, subject=args['subject'], message=args['message'], user_details=user_details)
    email_automation(args)
    logger.info("Email automation task completed")

scheduler = BlockingScheduler()
scheduler.add_job(schedule_email_automation, 'cron', hour=18, minute=23, timezone=timezone('Asia/Kolkata'))
scheduler.start()