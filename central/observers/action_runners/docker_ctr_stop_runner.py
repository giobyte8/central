import aiodocker
import logging
from typing import Any, Dict
from ..models import DockerCtrStopAction
from .base import ARunner
from central.utils import config as cfg


logger = logging.getLogger(__name__)


class DockerCtrStopRunner(ARunner):

    def __init__(self, action: DockerCtrStopAction):
        self.action = action

    async def run(self, context: Dict[str, Any]) -> None:
        logger.info(f'Running docker_ctr_stop action: { self.action.name }')

        try:
            d_client = aiodocker.Docker(url=cfg.docker_api_path())
            container = await d_client.containers.get(self.action.container)
            await container.stop()

            logger.info(
                f'Container stopped: { self.action.container }'
            )

            await d_client.close()
        except Exception as e:
            logger.error(
                'Error while stopping '
                f'container: { self.action.container } - { e }'
            )

