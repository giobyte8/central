import logging
from . import obs_dao as dao


logger = logging.getLogger(__name__)


def start():
    logger.info('Starting observers service...')
    observers = dao.find_all()


