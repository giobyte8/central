from central.api.models import HostStatus
from central.services import redis_svc
from uuid import UUID


async def save(host_id: UUID, status: HostStatus) -> None:
    await redis_svc.set_host_ip(host_id, status.ipv4Public)
