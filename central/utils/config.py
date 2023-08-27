import os
from dotenv import load_dotenv

load_dotenv()


def redis_host():
    return os.getenv('REDIS_HOST')

def redis_port():
    return os.getenv('REDIS_PORT')

def queue_notif():
    return os.getenv('QUEUE_NOTIFICATIONS')

def logs_path():
    return os.getenv('LOGS_PATH')

def log_level():
    return os.getenv('LOG_LEVEL', 'INFO')

def log_level_console():
    return os.getenv('LOG_LEVEL_CONSOLE', log_level())

def log_level_file():
    return os.getenv('LOG_LEVEL_FILE', log_level())

