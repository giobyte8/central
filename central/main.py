import asyncio
import os
import sys

# If package was not imported from other module
# and package has not been yet installed
if not __package__ and not hasattr(sys, "frozen"):
    central_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    sys.path.insert(0, os.path.realpath(central_root))

from central.api.ct_api import app as ct_api_app
from central.notif import notifier
from central.observers import observers_svc
from central.telegram import tg_bot


__ct_tasks = set()


@ct_api_app.before_serving
async def before_serving():
    bot_task = asyncio.create_task(tg_bot.start())
    notifier_task = asyncio.create_task(notifier.start())

    __ct_tasks.add(bot_task)
    __ct_tasks.add(notifier_task)


@ct_api_app.after_serving
async def shutdown():
    for task in __ct_tasks:
        task.cancel()


async def main():
    # You'll need to handle shutdown sequences for resources cleanup
    # await asyncio.gather(
    #     notifier.start(),
    #     observers_svc.start(),
    #     tg_bot.start(),

    #     # Use 'run_task' instead of 'run' to exec in an async
    #     # task that allows integration with other background
    #     # tasks.
    #     #serve(ct_api_app, Config()),
    #     #ct_api_app.run_task(host='0.0.0.0', port=5000)
    # )
    pass


if __name__ == '__main__':
    ct_api_app.run(host='0.0.0.0', port=5000)

    # Alternatively run all tasks into a custom coroutine
    # and start each task with asyncio.create_task() inside it.
    # See: https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently
    # ayncio.run(main())
