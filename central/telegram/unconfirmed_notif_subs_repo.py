from uuid import UUID
from central.services import redis_svc
from central.utils import config as cfg


async def save(sub_id: UUID) -> None:
    key = f'{ cfg.rd_tg_unconfirmed_notif_subs() }:{ sub_id }'

    # Set expiry to 10 mins
    secs_to_expire = 60 * 10

    await redis_svc.str_set(
        key,
        value=str(sub_id),
        expiry=secs_to_expire
    )


async def exists(sub_id: UUID) -> bool:
    key = f'{ cfg.rd_tg_unconfirmed_notif_subs() }:{ sub_id }'
    return await redis_svc.exists(key)


async def delete(sub_id: UUID) -> None:
    key = f'{ cfg.rd_tg_unconfirmed_notif_subs() }:{ sub_id }'
    await redis_svc.delete(key)

