from abc import ABCMeta, abstractmethod
from ..observer_jobs.base import ObserverJob


class Scheduler(metaclass=ABCMeta):

    @abstractmethod
    async def add_job(self, job: ObserverJob, interval: int):
        """Adds observer job to scheduler to be executed according
        to observer interval once scheduler is started.

        Args:
            job (ObserverJob): Observer job to schedule
            interval (int): Interval in seconds to execute the job
        """

    @abstractmethod
    async def start(self):
        """Starts the scheduler in background.

        When using same process workers (eg. Asyncio, ThreadPool, etc)
        this method will start workers execution as well.
        """
        pass
