import logging
import yaml

from ..errors import (
    ActionsInvalidConfigError,
    ActionNotFoundError,
    ObserversInvalidConfigError,
)
from ..models import (
    Action,
    RedisListRPushAction,
    RenderTemplateAction,
    DockerCtrStartAction,
    DockerCtrStopAction,
    Observer,
    RedisStringObserver,
    HttpStatusObserver,
)
from .memory import MemoryConfigStore
from central.utils import config as cfg
from central.utils import futils
from typing import Dict, List, Tuple


logger = logging.getLogger(__name__)


class _ConfigParser:
    """When reading config from Yaml or JSON files, values are retrieved
    as python dictionaries, use this class to parse such dicts and
    instantiate appropiate entity objects for config elements.
    """

    def parse(self, config: Dict) -> Tuple[List, List]:
        actions = []
        if 'actions' in config:
            actions = self.parse_actions(config['actions'])
        else:
            logger.info('No "actions" section found in config')

        observers = []
        if 'observers' in config:
            observers = self.parse_observers(config['observers'])
        else:
            logger.info('No "observers" section found in config')

        # TODO Verify that each observer's action exists

        return (observers, actions)

    def parse_actions(self, actions_cfg) -> List[Action]:
        actions = []

        if not type(actions_cfg) == dict:
            raise ActionsInvalidConfigError('Config must be a dictionary')

        for name in actions_cfg:
            if not 'type' in actions_cfg[name]:
                raise ActionsInvalidConfigError('Action type is missing')

            actions.append(self.parse_action(
                name,
                actions_cfg[name]
            ))

        return actions

    def parse_action(self, name: str, attrs: Dict) -> Action:
        a_type = attrs['type']

        # Add 'name' to rest of attributes so that we can
        # use pydantic to instantiate object
        attrs['name'] = name

        if a_type == 'redis_list_rpush':
            return RedisListRPushAction(**attrs)
        elif a_type == 'render_template':
            return RenderTemplateAction(**attrs)
        elif a_type == 'docker_ctr_start':
            return DockerCtrStartAction(**attrs)
        elif a_type == 'docker_ctr_stop':
            return DockerCtrStopAction(**attrs)
        else:
            raise ActionsInvalidConfigError(f'Invalid action type: { a_type }')

    def parse_observers(self, observers_cfg) -> List[Observer]:
        observers = []

        if not type(observers_cfg) == dict:
            raise ObserversInvalidConfigError('Config must be a dictionary')

        for name in observers_cfg:
            if not 'type' in observers_cfg[name]:
                raise ObserversInvalidConfigError('Observer type is missing')

            observers.append(self.parse_observer(
                name,
                observers_cfg[name]
            ))

        return observers

    def parse_observer(self, name: str, attrs: Dict) -> Observer:
        a_type = attrs['type']

        # Add 'name' to rest of attributes so that we can
        # use pydantic to instantiate object
        attrs['name'] = name

        if a_type == 'redis_string':
            return RedisStringObserver(**attrs)
        elif a_type == 'http_status':
            return HttpStatusObserver(**attrs)
        else:
            raise ObserversInvalidConfigError(
                f'Invalid observer type: { a_type }'
            )


class YamlConfigStore(MemoryConfigStore):
    """
    Observers and actions are loaded from yaml config file
    into memory during store initialization.

    Keeps loaded observers and actions as python objects
    in memory for fast access.
    """

    def __init__(self):
        super().__init__()
        self.__load_from_file()

    def __load_from_file(self) -> None:
        file_path = cfg.ct_config_file()
        futils.validate_file(file_path)

        logger.info(f'Loading config from: {file_path}')
        with open(file_path, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

            observers, actions = _ConfigParser().parse(config)
            self.add_actions(actions)

            self.verify_actions_existence(observers)
            self.add_observers(observers)

    def verify_actions_existence(self, observers: List[Observer]) -> None:
        for obs in observers:
            action_names: List[str] = []

            if type(obs) is RedisStringObserver:
                action_names = obs.on_change
            elif type(obs) is HttpStatusObserver:
                action_names = obs.on_unexpected_status

            for name in action_names:
                if not self.action_exists(name):
                    raise ActionNotFoundError(name)

    def reload(self) -> None:
        logger.info('Reloading config file')
        self.__load_from_file()
