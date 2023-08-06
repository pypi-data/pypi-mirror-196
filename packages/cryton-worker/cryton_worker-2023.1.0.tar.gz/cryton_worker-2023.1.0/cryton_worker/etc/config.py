from os import getenv, path, mkdir
from dotenv import load_dotenv


APP_DIRECTORY = getenv("CRYTON_WORKER_APP_DIRECTORY", path.expanduser("~/.local/cryton-worker/"))

load_dotenv(path.join(APP_DIRECTORY, ".env"))

LOG_DIRECTORY = path.join(APP_DIRECTORY, "log/")

for file_path in [APP_DIRECTORY, LOG_DIRECTORY]:
    if not path.exists(file_path):
        mkdir(file_path)

LOG_FILE_PATH = path.join(LOG_DIRECTORY, "cryton-worker.log")
LOG_FILE_PATH_DEBUG = path.join(LOG_DIRECTORY, "cryton-worker-debug.log")

WORKER_NAME = getenv("CRYTON_WORKER_NAME", "Worker")
MODULES_DIR = getenv("CRYTON_WORKER_MODULES_DIR")  # TODO: The default should point to the app directory
DEBUG = True if getenv("CRYTON_WORKER_DEBUG", "false").lower() == "true" else False
INSTALL_REQUIREMENTS = True if getenv("CRYTON_WORKER_INSTALL_REQUIREMENTS", "true").lower() == "true" else False
CONSUMER_COUNT = int(getenv("CRYTON_WORKER_CONSUMER_COUNT", 7))
PROCESSOR_COUNT = int(getenv("CRYTON_WORKER_PROCESSOR_COUNT", 7))
MAX_RETRIES = int(getenv("CRYTON_WORKER_MAX_RETRIES", 3))

MSFRPCD_HOST = getenv("CRYTON_WORKER_MSFRPCD_HOST", "127.0.0.1")
MSFRPCD_PORT = int(getenv("CRYTON_WORKER_MSFRPCD_PORT", 55553))
MSFRPCD_SSL = True if getenv("CRYTON_WORKER_MSFRPCD_SSL", "true").lower() == "true" else False
MSFRPCD_PASSWORD = getenv("CRYTON_WORKER_MSFRPCD_PASSWORD", "cryton")
MSFRPCD_USERNAME = getenv("CRYTON_WORKER_MSFRPCD_USERNAME", "cryton")

RABBIT_HOST = getenv("CRYTON_WORKER_RABBIT_HOST", "127.0.0.1")
RABBIT_PORT = int(getenv("CRYTON_WORKER_RABBIT_PORT", 5672))
RABBIT_USERNAME = getenv("CRYTON_WORKER_RABBIT_USERNAME", "cryton")
RABBIT_PASSWORD = getenv("CRYTON_WORKER_RABBIT_PASSWORD", "cryton")

EMPIRE_HOST = getenv("CRYTON_WORKER_EMPIRE_HOST", "127.0.0.1")
EMPIRE_PORT = int(getenv("CRYTON_WORKER_EMPIRE_PORT", 1337))
EMPIRE_USERNAME = getenv("CRYTON_WORKER_EMPIRE_USERNAME", "cryton")
EMPIRE_PASSWORD = getenv("CRYTON_WORKER_EMPIRE_PASSWORD", "cryton")
