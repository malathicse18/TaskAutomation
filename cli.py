from pymongo import MongoClient
import argparse
from email_automation import email_automation

def main():
    parser = argparse.ArgumentParser(description="📌 CLI Utility Tool - Automate various tasks")
    subparsers = parser.add_subparsers(dest="command", help="🔥 Available commands", required=True)

    email_parser = subparsers.add_parser(
        "email_automation",
        help="📧 Automate email sending",
        description="📧 Automate email sending\n\n"
                    "Example usage:\n"
                    "  python cli.py email_automation -f emails.csv -s 'Test Email' -m 'Hello!'\n"
                    "  python cli.py email_automation -f emails.csv -s 'Test Email' -m 'Hello!' --schedule '14:30'\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    email_parser.add_argument("-f", "--file", required=True, help="📂 CSV file with email addresses")
    email_parser.add_argument("-s", "--subject", required=True, help="📝 Email subject")
    email_parser.add_argument("-m", "--message", required=True, help="💬 Email message")
    email_parser.add_argument("--schedule", help="⏰ Schedule time in HH:MM format (24-hour clock)")
    email_parser.set_defaults(func=email_automation)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()