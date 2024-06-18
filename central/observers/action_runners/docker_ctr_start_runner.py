import aiodocker
import logging
from typing import Any, Dict
from ..models import DockerCtrStartAction
from .base import ARunner
from central.utils import config as cfg


logger = logging.getLogger(__name__)


class DockerCtrStartRunner(ARunner):

    def __init__(self, action: DockerCtrStartAction):
        self.action = action

    async def run(self, context: Dict[str, Any]) -> None:
        logger.info(f'Running docker_ctr_start action: { self.action.name }')

        try:
            d_client = aiodocker.Docker(url=cfg.docker_api_path())
            container = await d_client.containers.get(self.action.container)
            await container.start()

            logger.info(
                f'Container started: { self.action.container }'
            )

            await d_client.close()
        except Exception as e:
            logger.error(
                'Error while starting '
                f'container: { self.action.container } - { e }'
            )

