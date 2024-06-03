from abc import ABCMeta, abstractmethod

class ORunner(metaclass=ABCMeta):

    @abstractmethod
    def observe(self) -> None:
        """
        Executes required steps to verify status of
        this observer
        """

    @abstractmethod
    def run_actions(self) -> None:
        """
        Gets invoked when due to observation result, actions
        execution is required.
        """
