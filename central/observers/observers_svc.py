import logging
from .configstores.yaml import YamlConfigStore
from .observer_jobs import observer_job_from
from .scheduler.aps_aio_scheduler import AIOScheduler


logger = logging.getLogger(__name__)


async def start():
    logger.info('Starting observers service...')

    cfg_store = YamlConfigStore()
    observers = cfg_store.get_observers()
    scheduler = AIOScheduler()

    # Add each observer to scheduler
    for observer in observers:
        job = await observer_job_from(observer, cfg_store)
        if job is not None:
            await scheduler.add_job(job, observer.interval)
    await scheduler.start()
