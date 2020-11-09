from dotenv import load_dotenv
import os
import logging
load_dotenv()

BBGH_BACKEND_URL = os.getenv("BBGH_BACKEND_URL")
CACHE_DIR = dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/cache"

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

logging.basicConfig(level={
    'CRITICAL': logging.CRITICAL,
    'FATAL': logging.FATAL,
    'ERROR': logging.ERROR,
    'WARN': logging.WARNING,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET,
}[os.getenv("LOGGING_LEVEL").upper()])
