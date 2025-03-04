import argparse
import sys
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Add the project root directory (Automation) to sys.path
project_root = os.getenv("PROJECT_ROOT", os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.append(project_root)

from tasks.file_conversion import convert_files
from job_scheduler.scheduler import schedule_conversion

# Configure logging
log_file = os.path.join(project_root, "logs/cli.log")
logging.basicConfig(filename=log_file, level=logging.INFO,  # Set to INFO
                    format="%(asctime)s - %(levelname)s - %(message)s")

def file_conversion_cli(args):
    """Handles file conversion task"""
    convert_files(args.dir, args.ext, args.format)
    print(f"✅ File conversion completed for directory: {args.dir}")

def schedule_conversion_cli(args):
    """Handles scheduling of file conversion tasks"""
    schedule_conversion(args.dir, args.ext, args.format, args.mode, args.interval, args.run_date, args.cron_time)
    print(f"✅ Task scheduled successfully. Mode: {args.mode}")

def main():
    parser = argparse.ArgumentParser(
        description="Automation CLI Tool\n\n"
                    "Example usage:\n"
                    "  python cli/pycli/pycli.py file_conversion -h",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="task", help="Available tasks")
    
    # File Conversion Task
    fileconv_parser = subparsers.add_parser(
        "file_conversion",
        help="Convert files between formats",
        description="Convert files from one format to another.\n\n"
                    "Example usage:\n"
                    "  python cli/pycli/pycli.py file_conversion --dir '/home/user/docs' --ext txt --format pdf\n"
                    "  python cli/pycli/pycli.py file_conversion --dir 'C:\\path\\to\\files' --ext log --format json",
        formatter_class=argparse.RawTextHelpFormatter
    )
    fileconv_parser.add_argument("--dir", required=True, help="Directory containing files")
    fileconv_parser.add_argument("--ext", required=True, help="File extension to convert")
    fileconv_parser.add_argument("--format", required=True, help="Target file format")
    fileconv_parser.set_defaults(func=file_conversion_cli)

    # Schedule Conversion Task
    schedule_parser = subparsers.add_parser(
        "schedule_conversion",
        help="Schedule file conversion tasks",
        description="Schedule file conversion tasks with different modes.\n\n"
                    "Example usage:\n"
                    "  python cli/pycli/pycli.py schedule_conversion --dir '/home/user/docs' --ext txt --format pdf --mode interval --interval 10\n"
                    "  python cli/pycli/pycli.py schedule_conversion --dir 'C:\\path\\to\\files' --ext log --format json --mode cron --cron_time '14:30'\n"
                    "  python cli/pycli/pycli.py schedule_conversion --dir '/home/user/docs' --ext txt --format pdf --mode date --run_date '2025-03-03 14:30:00'\n"
                    "  python cli/pycli/pycli.py schedule_conversion --dir '/home/user/docs' --ext txt --format pdf --mode immediate",
        formatter_class=argparse.RawTextHelpFormatter
    )
    schedule_parser.add_argument("--dir", required=True, help="Directory containing files")
    schedule_parser.add_argument("--ext", required=True, help="File extension to convert")
    schedule_parser.add_argument("--format", required=True, help="Target file format")
    schedule_parser.add_argument("--mode", required=True, choices=["interval", "cron", "date", "immediate"], help="Scheduling mode")
    schedule_parser.add_argument("--interval", type=int, help="Interval in minutes for interval mode")
    schedule_parser.add_argument("--run_date", help="Run date and time for date mode (format: 'YYYY-MM-DD HH:MM:SS')")
    schedule_parser.add_argument("--cron_time", help="Time for cron mode (format: 'HH:MM')")
    schedule_parser.set_defaults(func=schedule_conversion_cli)

    args = parser.parse_args()

    if args.task:
        args.func(args)  # Execute the associated function
    else:
        parser.print_help()

if __name__ == "__main__":
    main()