from typing import Any, Dict


class ActionsSectionNotFound(Exception):
    def __init__(self, yaml_cfg: Dict) -> None:
        Exception.__init__(
            self,
            f'"actions" section wasn\'t found in yaml config: { yaml_cfg }'
        )

class ActionsSectionInvalid(Exception):
    def __init__(self, actions_cfg: Any) -> None:
        Exception.__init__(
            self,
            f'"actions" section isn\'t a valid list: { actions_cfg }'
        )

class ActionsValidationError(Exception):
    def __init__(self, msg: str) -> None:
        Exception.__init__(
            self,
            f'Actions definition is invalid: { msg }'
        )

class ObserversSectionNotFound(Exception):
    def __init__(self, yaml_cfg: Dict) -> None:
        Exception.__init__(
            self,
            f'"observers" section wasn\'t found in yaml config: { yaml_cfg }'
        )

class ObserversSectionInvalid(Exception):
    def __init__(self, actions_cfg: Any) -> None:
        Exception.__init__(
            self,
            f'"observers" section isn\'t a valid list: { actions_cfg }'
        )

class ObserversValidationError(Exception):
    def __init__(self, msg: str) -> None:
        Exception.__init__(
            self,
            f'Observers definition is invalid: { msg }'
        )
