import time
from .scheduler import scheduled_task

def run_scheduler():
    while True:
        scheduled_task()
        time.sleep(60)  # Run every minute

if __name__ == "__main__":
    run_scheduler()