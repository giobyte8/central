from abc import ABCMeta, abstractmethod
from typing import Any, Dict


class ObserverJob(metaclass=ABCMeta):

    @abstractmethod
    async def observe(self) -> None:
        """
        Executes required steps to verify status of
        this observer
        """

    @abstractmethod
    async def run_actions(self, context: Dict[str, Any]) -> None:
        """Gets invoked when, due to observation result, actions
        execution is required.

        Args:
            context (Dict[str, Any]): Context data passed to actions \
                runners for execution
        """
