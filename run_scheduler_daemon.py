import daemon
import logging
from scheduler import run_scheduler

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler_daemon.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run():
    logger.info("Starting scheduler daemon")
    run_scheduler()

if __name__ == "__main__":
    with daemon.DaemonContext():
        run()