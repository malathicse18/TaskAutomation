# database.py
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['file_conversion_db']

def save_conversion_task(input_file, output_file, status):
    task = {
        "input_file": input_file,
        "output_file": output_file,
        "status": status
    }
    db.conversion_tasks.insert_one(task)
    print(f"Saved task: {task}")