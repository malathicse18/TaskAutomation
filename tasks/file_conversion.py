import os
import pandas as pd
import logging
from db.logs_collection import log_task

# Ensure logs directory exists
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs"))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logging to use db.log
log_file = os.path.join(log_dir, "db.log")
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,  # Set to DEBUG for troubleshooting
    format="%(asctime)s - %(levellevel)s - %(message)s"
)

def convert_files(directory, ext, format):
    """Convert files from one format to another."""
    try:
        print("Starting file conversion process")
        logging.info("Starting file conversion process")
        converted_files = []

        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")

        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)

            if os.path.isfile(file_path) and file.endswith(f".{ext}"):
                src = file_path
                dst = os.path.join(directory, file.replace(f".{ext}", f".{format}"))

                logging.info(f"Processing file: {src}")

                if not os.access(src, os.R_OK):
                    logging.error(f"Permission denied: {src}")
                    continue

                try:
                    if os.path.getsize(src) == 0:
                        # Create an empty target file if the source file is empty
                        open(dst, 'w').close()
                        logging.info(f"Converted empty file: {src} → {dst}")
                    else:
                        df = pd.read_csv(src, delimiter="\t")
                        df.to_csv(dst, index=False)
                        logging.info(f"Converted: {src} → {dst}")

                    converted_files.append(dst)
                except pd.errors.ParserError:
                    logging.error(f"Parsing error in file: {src}")
                except Exception as file_error:
                    logging.error(f"Error converting {src}: {file_error}")

        status = "Success" if converted_files else "No files converted"
        log_task(directory, ext, format, status, f"Converted {len(converted_files)} files")
        logging.info("File conversion process completed")
    except Exception as e:
        log_task(directory, ext, format, "Failed", str(e))
        logging.error(f"Conversion failed: {e}")