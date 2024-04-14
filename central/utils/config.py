import os
from dotenv import load_dotenv

load_dotenv()


def env_mode() -> str:
    return os.getenv('ENV_MODE', 'dev')

def redis_host():
    return os.getenv('REDIS_HOST')

def redis_port():
    return os.getenv('REDIS_PORT')

def redis_ssl() -> bool:
    return os.getenv('REDIS_SSL', 'false') == 'true'

def redis_username() -> str:
    return os.getenv('REDIS_USERNAME')

def redis_password() -> str:
    return os.getenv('REDIS_PASSWORD')

def rd_prefix():
    return os.getenv('RD_PREFIX')

def rd_tg_unconfirmed_notif_subs() -> str:
    return os.getenv('RD_TG_UNCONFIRMED_NOTIF_SUBS')

def rd_tg_notif_subscribed_chats() -> str:
    return os.getenv('RD_TG_NOTIF_SUBSCRIBED_CHATS')

def queue_notif():
    return os.getenv('QUEUE_NOTIFICATIONS')


def allowed_hosts():
    ids = os.getenv('ALLOWED_HOSTS', '')
    return ids.split()


def api_jwt_secret_key():
    return os.getenv('API_JWT_SECRET_KEY')

def notif_feed_subs_pwd():
    return os.getenv('NOTIF_FEED_SUBSCRIPTION_PWD')


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
