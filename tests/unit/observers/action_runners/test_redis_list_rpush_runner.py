import pytest
from unittest.mock import AsyncMock, patch
from central.observers.action_runners.redis_list_rpush_runner import (
    RedisListRPushRunner
)
from central.observers.models import RedisListRPushAction


_TGT_MODULE = 'central.observers.action_runners.redis_list_rpush_runner'


class TestRedisListRPushRunner:

    @pytest.mark.asyncio
    @patch(f'{ _TGT_MODULE }.redis_svc.list_rpush')
    async def test_run_with_single_argument(self, m_rd_lrpush: AsyncMock):
        action = RedisListRPushAction(
            name='t_action',
            list_key='t_key',
            msg_template='Hello {{ name }}!'
        )
        action_runner = RedisListRPushRunner(action)

        await action_runner.run({'name': 'World'})
        m_rd_lrpush.assert_called_once_with('t_key', 'Hello World!')
