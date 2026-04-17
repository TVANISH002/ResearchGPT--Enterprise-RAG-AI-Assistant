import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("RAGApp")

def log_info(msg):
    print(msg)
    logger.info(msg)

def log_error(msg):
    print(f"ERROR: {msg}")
    logger.error(msg)