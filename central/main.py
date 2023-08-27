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

from central.notif import notifier


async def main():
    await asyncio.gather(
        notifier.start()
    )


if __name__ == '__main__':
    asyncio.run(main())

