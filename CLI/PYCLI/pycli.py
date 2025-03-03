import argparse
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root directory (Automation) to sys.path
project_root = os.getenv("PROJECT_ROOT", os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.append(project_root)

from tasks.file_conversion import convert_files

def file_conversion_cli(args):
    """Handles file conversion task"""
    convert_files(args.dir, args.ext, args.format)
    print(f"✅ File conversion completed for directory: {args.dir}")

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

    args = parser.parse_args()

    if args.task:
        args.func(args)  # Execute the associated function
    else:
        parser.print_help()

if __name__ == "__main__":
    main()