import argparse
import uuid
import time
from datetime import datetime, timedelta
from config import EMAIL_SENDER
from database import save_user_details_in_task, save_csv_data_to_db, save_email_task, save_web_scraping_task, store_gold_rate
from tasks.email_automation import process_email_task
from tasks.file_conversion import file_conversion
from tasks.log_compression import log_compression
from tasks.log_deletion import log_deletion
from tasks.web_scraping import scrape_website
import logging

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

def schedule_email_automation(args):
    logger.info("Email automation task started")
    user_id = f"{args.user_email}_{uuid.uuid4()}"
    csv_data = save_csv_data_to_db(args.file, user_id)
    user_details = save_user_details_in_task(
        user_id=user_id, name=args.user_name, email=EMAIL_SENDER, preferences={}, csv_data=csv_data
    )
    save_email_task(
        emails=csv_data, subject=args.subject, message=args.message, user_details=user_details,
        schedule_hour=args.schedule_hour, schedule_minute=args.schedule_minute, frequency=args.frequency
    )
    logger.info("Email automation task completed")

def wait_until_schedule(hour, minute):
    now = datetime.now()
    scheduled_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if scheduled_time < now:
        scheduled_time += timedelta(days=1)
    wait_time = (scheduled_time - now).total_seconds()
    logger.info(f"Waiting for {wait_time} seconds until the scheduled time.")
    time.sleep(wait_time)

def web_scraping(args):
    user_id = f"example_user_{uuid.uuid4()}"
    user_details = {"user_id": user_id, "name": "Example User", "email": EMAIL_SENDER}

    gold_data = scrape_website(args.url)
    logger.info(f"Scraped Data: {gold_data}")

    if gold_data:
        try:
            store_gold_rate(gold_data)
            save_web_scraping_task(args.url, gold_data, user_details)
            logger.info("Gold rate data stored successfully.")
        except Exception as e:
            logger.error(f"Error storing data: {e}", exc_info=True)
    else:
        logger.error("Failed to scrape gold rate data.")

def main():
    parser = argparse.ArgumentParser(description="📌 CLI Utility Tool - Automate various tasks")
    subparsers = parser.add_subparsers(dest="command", help="🔥 Available commands", required=True)

    email_parser = subparsers.add_parser(
        "email_automation",
        help="📧 Automate email sending",
        description="📧 Automate email sending\n\n"
                    "Example usage:\n"
                    " python cli.py email_automation -f emails.csv -s 'Test Email' -m 'Hello!' --user_name 'John Doe'\n"
                    " python cli.py email_automation -f emails.csv -s 'Test Email' -m 'Hello!' --schedule_hour 14 --schedule_minute 30 --frequency daily --user_name 'John Doe'\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    email_parser.add_argument("-f", "--file", required=True, help="📂 CSV file with email addresses")
    email_parser.add_argument("-s", "--subject", required=True, help="📝 Email subject")
    email_parser.add_argument("-m", "--message", required=True, help="💬 Email message")
    email_parser.add_argument("--schedule_hour", type=int, help="⏰ Schedule hour (0-23)")
    email_parser.add_argument("--schedule_minute", type=int, help="⏰ Schedule minute (0-59)")
    email_parser.add_argument("--frequency", choices=['daily', 'weekly'], help="🔄 Frequency of the email task")
    email_parser.add_argument("--user_name", required=True, help="👤 User name")
    email_parser.set_defaults(func=schedule_email_automation)

    file_conversion_parser = subparsers.add_parser(
        "file_conversion",
        help="🔄 Automate file conversion",
        description="🔄 Automate file conversion\n\n"
                    "Example usage:\n"
                    " python cli.py file_conversion -i input.txt -o output.pdf\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    file_conversion_parser.add_argument("-i", "--input", required=True, help="📂 Input file")
    file_conversion_parser.add_argument("-o", "--output", required=True, help="📂 Output file")
    file_conversion_parser.set_defaults(func=file_conversion)

    log_compression_parser = subparsers.add_parser(
        "log_compression",
        help="📦 Automate log compression",
        description="📦 Automate log compression\n\n"
                    "Example usage:\n"
                    " python cli.py log_compression -d /path/to/logs\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    log_compression_parser.add_argument("-d", "--directory", required=True, help="📂 Directory with logs")
    log_compression_parser.set_defaults(func=log_compression)

    log_deletion_parser = subparsers.add_parser(
        "log_deletion",
        help="🗑️ Automate log deletion",
        description="🗑️ Automate log deletion\n\n"
                    "Example usage:\n"
                    " python cli.py log_deletion -d /path/to/logs\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    log_deletion_parser.add_argument("-d", "--directory", required=True, help="📂 Directory with logs")
    log_deletion_parser.set_defaults(func=log_deletion)

    web_scraping_parser = subparsers.add_parser(
        "web_scraping",
        help="🌐 Automate web scraping",
        description="🌐 Automate web scraping and store gold rates.\n\n"
                    "Example usage:\n"
                    " python cli.py web_scraping -u <URL>\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    web_scraping_parser.add_argument("-u", "--url", required=True, help="🔗 URL of the website to scrape")
    web_scraping_parser.set_defaults(func=web_scraping)

    args = parser.parse_args()

    if args.command == "email_automation":
        args.user_email = EMAIL_SENDER
        user_id = f"{args.user_email}_{uuid.uuid4()}"
        csv_data = save_csv_data_to_db(args.file, user_id)
        user_details = save_user_details_in_task(
            user_id=user_id, name=args.user_name, email=EMAIL_SENDER, preferences={}, csv_data=csv_data
        )
        save_email_task(
            emails=csv_data, subject=args.subject, message=args.message, user_details=user_details,
            schedule_hour=args.schedule_hour, schedule_minute=args.schedule_minute, frequency=args.frequency
        )
        logger.info(f"Scheduled email automation task for {args.user_name} at {args.schedule_hour}:{args.schedule_minute} {args.frequency}")
        user_details['subject'] = args.subject  # Ensure the subject key is included
        user_details['message'] = args.message  # Ensure the message key is included

        if args.schedule_hour is not None and args.schedule_minute is not None:
            wait_until_schedule(args.schedule_hour, args.schedule_minute)  # Wait until the scheduled time

        process_email_task(user_details)  # Process the email task immediately

    try:
        if args.command != "email_automation":
            args.func(vars(args))  # Pass the arguments as a dictionary
    except Exception as e:
        logger.error(f"A general error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()