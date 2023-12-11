"""Exposes functionality to load, parse and access observers \
    and actions config from yaml files
"""
import logging
import yaml
from .errors import (
    ObserversSectionInvalid,
    ObserversValidationError,
)
from .models import CTObserver, observersAdapter
from central.utils import config as cfg
from central.utils import futils
from typing import Dict, List


logger = logging.getLogger(__name__)


class InMemoryStore:
    def __init__(self) -> None:
        self.initialized = False
        self.observers: List[CTObserver] = []

    def __init_from_yaml(self):
        logger.debug('Loading observers from yaml')

        cfg_file = cfg.ct_config_file()
        futils.validate_file(cfg_file)
        with open(cfg_file, 'r') as f:
            ct_config = yaml.load(f, Loader=yaml.FullLoader)
            self.__parse_observers(ct_config)

        self.initialized = True

    def __parse_observers(self, ct_config: Dict) -> None:
        if 'observers' not in ct_config:
            logger.debug('No "observers" section found in config')
            return

        observers_cfg = ct_config['observers']
        if observers_cfg is None:
            logger.warning('Empty "observers" section found in config')
            return

        if type(observers_cfg) is not list:
            raise ObserversSectionInvalid(observers_cfg)

        # Deserialize observers
        try:
            self.observers = observersAdapter.validate_python(observers_cfg)
        except ValueError as e:
            # Wrap into custom ActionsValidationError
            raise ObserversValidationError(str(e))
        logger.debug('Loaded observers: %s', self.observers)

    def find_all_observers(self) -> List[CTObserver]:
        if not self.initialized:
            self.__init_from_yaml()
        return self.observers


_dstore = InMemoryStore()


def all() -> List[CTObserver]:
    return _dstore.find_all_observers()
