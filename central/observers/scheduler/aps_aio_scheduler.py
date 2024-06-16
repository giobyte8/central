import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .base import Scheduler
from ..observer_jobs.base import ObserverJob


logger = logging.getLogger(__name__)


class AIOScheduler(Scheduler):
    """Uses apscheduler 3.x library and asyncio for workers.
    Jobs are keep in memory, no persistent storage is used.
    """

    def __init__(self):
        self._scheduler = AsyncIOScheduler()

    async def add_job(self, job: ObserverJob, interval: int):
        self._scheduler.add_job(
            job.observe,
            'interval',
            seconds=interval
        )

    async def start(self):
        self._scheduler.start()
