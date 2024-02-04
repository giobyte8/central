import os
from dotenv import load_dotenv

load_dotenv()


def redis_host():
    return os.getenv('REDIS_HOST')

def redis_port():
    return os.getenv('REDIS_PORT')

def redis_keys_prefix():
    return os.getenv('REDIS_KEYS_PREFIX')

def queue_notif():
    return os.getenv('QUEUE_NOTIFICATIONS')


def allowed_hosts():
    ids = os.getenv('ALLOWED_HOSTS', '')
    return ids.split()


def api_jwt_secret_key():
    return os.getenv('API_JWT_SECRET_KEY')


def tg_bot_token():
    return os.getenv('TELEGRAM_BOT_TOKEN')

def tg_web_apps_url():
    return os.getenv('TELEGRAM_WEB_APPS_URL')


def logs_path():
    return os.getenv('LOGS_PATH')

def log_level():
    return os.getenv('LOG_LEVEL', 'INFO')

def log_level_console():
    return os.getenv('LOG_LEVEL_CONSOLE', log_level())

def log_level_file():
    return os.getenv('LOG_LEVEL_FILE', log_level())


def ct_config_file():
    return os.getenv('CT_CONFIG_FILE')
