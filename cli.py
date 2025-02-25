import argparse
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from tasks.file_conversion import file_conversion as convert_files

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def schedule_file_conversion(args):
    scheduler = BlockingScheduler()

    def scheduled_task():
        try:
            convert_files(args)
            logger.info("File conversion task completed successfully.")
        except Exception as e:
            logger.error(f"Error during file conversion: {e}")

    if args.frequency == 'daily':
        scheduler.add_job(scheduled_task, 'interval', days=1)
    elif args.frequency == 'hourly':
        scheduler.add_job(scheduled_task, 'interval', hours=1)
    elif args.frequency == 'weekly':
        scheduler.add_job(scheduled_task, 'interval', weeks=1)
    elif args.frequency == '2mins':
        scheduler.add_job(scheduled_task, 'interval', minutes=2)
    else:
        logger.error("Invalid frequency. Please choose 'daily', 'hourly', 'weekly', or '2mins'.")
        return

    logger.info("Scheduler started.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

def file_conversion(args):
    if args.frequency:
        schedule_file_conversion(args)
    else:
        convert_files(args)

def main():
    parser = argparse.ArgumentParser(description="📌 CLI Utility Tool - Automate various tasks")
    subparsers = parser.add_subparsers(dest="command", help="🔥 Available commands", required=True)

    file_conversion_parser = subparsers.add_parser(
        "file_conversion",
        help="🔄 Automate file conversion",
        description="🔄 Automate file conversion\n\n"
                    "Example usage:\n"
                    " python cli.py file_conversion -d input_directory --frequency 2mins\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    file_conversion_parser.add_argument("-d", "--input_directory", required=True, help="📂 Input directory containing text files")
    file_conversion_parser.add_argument("--frequency", choices=['daily', 'hourly', 'weekly', '2mins'], help="🔄 Frequency of the task")
    file_conversion_parser.set_defaults(func=file_conversion)

    args = parser.parse_args()

    try:
        args.func(args)
    except Exception as e:
        logger.error(f"A general error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()