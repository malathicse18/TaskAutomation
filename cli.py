import argparse
from email_automation import email_automation
from tasks.web_scraping import web_scraping
from tasks.log_compression import log_compression
from tasks.log_deletion import log_deletion
from tasks.file_conversion import file_conversion

def main():
    parser = argparse.ArgumentParser(description="📌 CLI Utility Tool - Automate various tasks")
    subparsers = parser.add_subparsers(dest="command", help="🔥 Available commands", required=True)

    # 📧 Email Automation
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
    email_parser.add_argument("-a", "--attachment", help="📎 File to attach (optional)")
    email_parser.add_argument("--schedule", help="⏰ Schedule time in HH:MM format (24-hour clock)")
    email_parser.set_defaults(func=email_automation)

    # 🌐 Web Scraping
    web_parser = subparsers.add_parser("web_scraping", help="🌐 Scrape data from websites")
    web_parser.set_defaults(func=web_scraping)

    # 📦 Log Compression
    log_compression_parser = subparsers.add_parser("log_compression", help="📦 Compress log files")
    log_compression_parser.set_defaults(func=log_compression)

    # 🗑️ Log Deletion
    log_deletion_parser = subparsers.add_parser("log_deletion", help="🗑️ Delete old log files")
    log_deletion_parser.set_defaults(func=log_deletion)

    # 🔄 File Conversion
    file_conversion_parser = subparsers.add_parser("file_conversion", help="🔄 Convert files")
    file_conversion_parser.set_defaults(func=file_conversion)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()