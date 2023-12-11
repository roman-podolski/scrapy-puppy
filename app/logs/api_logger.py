import logging
from datetime import datetime
from logging.handlers import WatchedFileHandler

from app.conf.configuration import config

# log_path = config["Log"]["api_log_path"]
# new_log_file_name_for_loguru = log_path.replace(".log", f'{datetime.now().strftime("%Y%m%dT%H:%M")}.log')

logger = logging.getLogger(__name__)
handlers = [logging.StreamHandler()]
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s\t%(filename)s\t%(funcName)s: %(message)s", handlers=handlers
)

