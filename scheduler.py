from apscheduler.schedulers.blocking import BlockingScheduler
from tasks.file_conversion import file_conversion
import logging
import argparse
import signal
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def scheduled_task():
    try:
        args = argparse.Namespace(input='input.txt', output='output.pdf')
        file_conversion(args)
        logger.info("File conversion task completed successfully.")
    except Exception as e:
        logger.error(f"Error during file conversion: {e}")

def signal_handler(sig, frame):
    logger.info("Exiting scheduler...")
    scheduler.shutdown()
    sys.exit(0)

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    
    # Schedule the task based on user input
    user_input = input("Enter schedule frequency (daily/hourly/weekly): ").strip().lower()
    if user_input == 'daily':
        scheduler.add_job(scheduled_task, 'interval', days=1)
    elif user_input == 'hourly':
        scheduler.add_job(scheduled_task, 'interval', hours=1)
    elif user_input == 'weekly':
        scheduler.add_job(scheduled_task, 'interval', weeks=1)
    else:
        logger.error("Invalid input. Please choose 'daily', 'hourly', or 'weekly'.")
        exit(1)
    
    logger.info("Scheduler started.")
    
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass