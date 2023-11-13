import logging
from central.api.models import HostStatus
from central.dao import host_status_dao
from central.utils import config as cfg
from uuid import UUID


logger = logging.getLogger(__name__)

async def update(host_id: UUID, status: HostStatus) -> None:
    """Persists host status to redis

    Args:
        status (HostStatus): Host status
    """

    if is_host_allowed(host_id):
        await host_status_dao.save(host_id, status)
    else:
        logger.error(
            'Host "%s" is not in the list of allowed hosts',
            host_id
        )


def is_host_allowed(host_id: UUID) -> bool:
    return str(host_id) in cfg.allowed_hosts()
