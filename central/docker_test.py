import asyncio
import aiodocker


async def main():
    d_client = aiodocker.Docker(url='unix:///var/run/docker.sock')

    print('Running containers:')
    containers = await d_client.containers.list()
    for container in containers:
        print(container._container['Names'][0])

    c_rabbitmq = await d_client.containers.get('rabbitmq')
    await c_rabbitmq.stop()

    print('\nRunning containers:')
    containers = await d_client.containers.list()
    for container in containers:
        print(container)

    await d_client.close()


if __name__ == '__main__':
    asyncio.run(main())
