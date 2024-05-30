from typing import List, Optional
from ..errors import ConfigStoreError
from ..models import Action, Observer
from .base import ConfigStore


class MemoryConfigStore(ConfigStore):

    def __init__(self) -> None:
        super().__init__()
        self._actions: List[Action] = []
        self._observers: List[Observer] = []

    def add_observers(self, observers: List[Observer]) -> None:
        for observer in observers:
            self.add_observer(observer)

    def add_observer(self, observer: Observer) -> None:
        if self.observer_exists(observer.name):
            raise ConfigStoreError(
                f'An observer named "{ observer.name }" already exists'
            )
        self._observers.append(observer)

    def observer_exists(self, name: str) -> bool:
        return any(o.name == name for o in self._observers)

    def get_observers(self) -> List[Observer]:
        return self._observers


    def add_actions(self, actions: List[Action]) -> None:
        for action in actions:
            self.add_action(action)

    def add_action(self, action: Action) -> None:
        if self.action_exists(action.name):
            raise ConfigStoreError(
                f'An action named "{ action.name }" already exists'
            )
        self._actions.append(action)

    def find_action(self, name: str) -> Optional[Action]:
        for a in self._actions:
            if a.name == name:
                return a
        return None

    def action_exists(self, name: str) -> bool:
        return any(a.name == name for a in self._actions)
