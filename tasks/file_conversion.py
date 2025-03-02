import os
import pandas as pd
import logging
from db.logs_collection import log_task

# Configure logging
logging.basicConfig(filename="logs/conversion.log", level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def convert_files(directory, ext, format):
    """Convert files from one format to another."""
    try:
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
                    df = pd.read_csv(src, delimiter="\t")
                    df.to_csv(dst, index=False)
                    converted_files.append(dst)
                    logging.info(f"Converted: {src} → {dst}")
                except Exception as file_error:
                    logging.error(f"Error converting {src}: {file_error}")

        log_task(directory, ext, format, "Success", f"Converted {len(converted_files)} files")
        logging.info("File conversion process completed")
    except Exception as e:
        log_task(directory, ext, format, "Failed", str(e))
        logging.error(f"Conversion failed: {e}")
