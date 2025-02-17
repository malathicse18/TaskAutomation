import argparse
import uuid
from pymongo import MongoClient
from tasks.email_automation import email_automation
from tasks.file_conversion import file_conversion
from tasks.log_compression import log_compression
from tasks.log_deletion import log_deletion
from tasks.web_scraping import web_scraping_task  # Updated import
from config import EMAIL_SENDER  # Assuming EMAIL_SENDER is the sender's email
from database import save_user_details_in_task, save_csv_data_to_db, save_email_task  # Import necessary functions

def web_scraping(args):
    user_details = {"user_id": "example_user_id"}  # Replace with actual user details
    web_scraping_task(args.keyword, user_details)

def main():
    parser = argparse.ArgumentParser(description="📌 CLI Utility Tool - Automate various tasks")
    subparsers = parser.add_subparsers(dest="command", help="🔥 Available commands", required=True)

    # Email Automation
    email_parser = subparsers.add_parser(
        "email_automation",
        help="📧 Automate email sending",
        description="📧 Automate email sending\n\n"
                    "Example usage:\n"
                    "  python cli.py email_automation -f emails.csv -s 'Test Email' -m 'Hello!' --user_name 'John Doe'\n"
                    "  python cli.py email_automation -f emails.csv -s 'Test Email' -m 'Hello!' --schedule '14:30' --user_name 'John Doe'\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    email_parser.add_argument("-f", "--file", required=True, help="📂 CSV file with email addresses")
    email_parser.add_argument("-s", "--subject", required=True, help="📝 Email subject")
    email_parser.add_argument("-m", "--message", required=True, help="💬 Email message")
    email_parser.add_argument("--schedule", help="⏰ Schedule time in HH:MM format (24-hour clock)")
    email_parser.add_argument("--user_name", required=True, help="👤 User name")
    email_parser.set_defaults(func=email_automation)

    # File Conversion
    file_conversion_parser = subparsers.add_parser(
        "file_conversion",
        help="🔄 Automate file conversion",
        description="🔄 Automate file conversion\n\n"
                    "Example usage:\n"
                    "  python cli.py file_conversion -i input.txt -o output.pdf\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    file_conversion_parser.add_argument("-i", "--input", required=True, help="📂 Input file")
    file_conversion_parser.add_argument("-o", "--output", required=True, help="📂 Output file")
    file_conversion_parser.set_defaults(func=file_conversion)

    # Log Compression
    log_compression_parser = subparsers.add_parser(
        "log_compression",
        help="📦 Automate log compression",
        description="📦 Automate log compression\n\n"
                    "Example usage:\n"
                    "  python cli.py log_compression -d /path/to/logs\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    log_compression_parser.add_argument("-d", "--directory", required=True, help="📂 Directory with logs")
    log_compression_parser.set_defaults(func=log_compression)

    # Log Deletion
    log_deletion_parser = subparsers.add_parser(
        "log_deletion",
        help="🗑️ Automate log deletion",
        description="🗑️ Automate log deletion\n\n"
                    "Example usage:\n"
                    "  python cli.py log_deletion -d /path/to/logs\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    log_deletion_parser.add_argument("-d", "--directory", required=True, help="📂 Directory with logs")
    log_deletion_parser.set_defaults(func=log_deletion)

    # Web Scraping (Updated for Keyword Search)
    web_scraping_parser = subparsers.add_parser(
        "web_scraping",
        help="🌐 Automate web scraping",
        description="🌐 Automate web scraping based on keywords\n\n"
                    "Example usage:\n"
                    "  python cli.py web_scraping -k 'Python Programming' -o output.csv\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    web_scraping_parser.add_argument("-k", "--keyword", required=True, help="🔍 Keyword to search")
    web_scraping_parser.add_argument("-o", "--output", required=True, help="📂 Output file")
    web_scraping_parser.set_defaults(func=web_scraping)

    args = parser.parse_args()

    # Process email automation: Save user details and emails in the database
    if args.command == "email_automation":
        args.user_email = EMAIL_SENDER
        user_id = f"{args.user_email}_{uuid.uuid4()}"  # Generate a unique user ID
        csv_data = save_csv_data_to_db(args.file, user_id)
        user_details = save_user_details_in_task(
            user_id=user_id, name=args.user_name, email=EMAIL_SENDER, preferences={}, csv_data=csv_data
        )
        save_email_task(emails=csv_data, subject=args.subject, message=args.message, user_details=user_details)

    args.func(args)

if __name__ == "__main__":
    main()