
class ActionNotFoundError(Exception):
    """Raised by data stores when an observer action is not found"""

    def __init__(self, action_name: str) -> None:
        super().__init__(self, f'Action {action_name} not found')


class ActionsInvalidConfigError(Exception):
    """Raised during parsing of YAML config"""


class ObserversInvalidConfigError(Exception):
    """Raised during parsing of YAML config"""


class ConfigStoreError(Exception):
    """Raised by stores during CRUD operations"""
