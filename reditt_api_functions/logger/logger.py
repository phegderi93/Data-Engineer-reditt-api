import logging
import os


log_dir = 'logs'

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "app.log")),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
