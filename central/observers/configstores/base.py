from abc import ABCMeta, abstractmethod
from typing import List
from ..models import Action, Observer


class ConfigStore(metaclass=ABCMeta):

    @abstractmethod
    def add_observers(self, observers: List[Observer]) -> None:
        """Adds multiple observers to store

        Args:
            observers (List[Observer]): Observers to add
        """

    @abstractmethod
    def add_observer(self, observer: Observer) -> None:
        """Adds a single observer to store

        Args:
            observer (Observer): Observer to add
        """

    @abstractmethod
    def get_observers(self) -> List[Observer]:
        """Retries all configured observers

        Returns:
            List[Observer]: Configured observers
        """

    @abstractmethod
    def observer_exists(self, name: str) -> bool:
        """Checks if an observer with given name exists

        Args:
            name (str): Observer's name

        Returns:
            bool: True if an observer was found
        """


    @abstractmethod
    def add_actions(self, actions: List[Action]) -> None:
        """Adds multiple actions to store

        Args:
            actions (List[Action]): Actions to add
        """

    @abstractmethod
    def add_action(self, action: Action) -> None:
        """Adds a single action to store

        Args:
            action (Action): Action to add
        """

    @abstractmethod
    def find_action(self, name: str) -> Action:
        """Finds an action by name

        Args:
            name (str): Name of the action to find

        Returns:
            Action: Found action
        """

    @abstractmethod
    def action_exists(self, name: str) -> bool:
        """Checks if an action with given name exists

        Args:
            name (str): Action's name

        Returns:
            bool: True if an action was found
        """
