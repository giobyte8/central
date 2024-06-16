from abc import ABCMeta, abstractmethod
from typing import Any, Dict


class ARunner(metaclass=ABCMeta):

    @abstractmethod
    async def run(self, context: Dict[str, Any]) -> None:
        """Runs action

        Args:
            context (Dict[str, Any]): A dictionary of context passed by \
                caller, such values would be used during execution.
        """
