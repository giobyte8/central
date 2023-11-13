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
from central.telegram import tg_bot


async def main():
    await asyncio.gather(
        notifier.start(),
        tg_bot.start()
    )


if __name__ == '__main__':
    # asyncio.run(main())
    ct_api_app.run(host='0000000', port=5000)

