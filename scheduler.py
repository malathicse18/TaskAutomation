import logging
from .tasks.email_automation import process_email_task
from .database import get_email_tasks

logging.basicConfig(filename='scheduler.log', level=logging.INFO)

def scheduled_task():
    tasks = get_email_tasks()
    for task in tasks:
        process_email_task(task)