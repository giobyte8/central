import pytest
from unittest.mock import Mock, patch
from central.observers.action_runners.base import ARunner
from central.observers.observer_jobs.redis_str import RedisStrObserverJob
from central.observers.models import RedisStringObserver


class TestRedisStrObserverJob:

    @pytest.mark.asyncio
    @patch('central.observers.observer_jobs.redis_str.redis_svc.str_set')
    @patch(
        'central.observers.observer_jobs.redis_str.redis_svc.str_get',
        side_effect=[None, 'key_curr_value']
    )
    async def test_observe_no_previous_value(self, m_str_get: Mock, m_str_set: Mock):
        obs = RedisStringObserver(
            name='test',
            interval=5,
            key='test_key',
            on_change=['fake_test_action']
        )
        job = RedisStrObserverJob(obs, [])

        await job.observe()

        assert m_str_get.call_count == 2
        m_str_set.assert_called_once_with(f'{ obs.key }.last', 'key_curr_value')

    @pytest.mark.asyncio
    @patch('central.observers.observer_jobs.redis_str.redis_svc.str_set')
    @patch(
        'central.observers.observer_jobs.redis_str.redis_svc.str_get',
        side_effect=['same_value', 'same_value']
    )
    async def test_observe_value_didnt_change(self, m_str_get: Mock, m_str_set: Mock):
        obs = RedisStringObserver(
            name='test',
            interval=5,
            key='t_key',
            on_change=['1', '2']
        )

        # Create and run observer job
        job = RedisStrObserverJob(obs, [])
        await job.observe()

        # Assert calls to redis service
        assert m_str_get.call_count == 2
        m_str_set.assert_not_called()

    @pytest.mark.asyncio
    @patch('central.observers.observer_jobs.redis_str.redis_svc.str_set')
    @patch(
        'central.observers.observer_jobs.redis_str.redis_svc.str_get',
        side_effect=['old_value', 'new_value']
    )
    async def test_observe_value_changed(self, m_str_get: Mock, m_str_set: Mock):
        obs = RedisStringObserver(
            name='test',
            interval=5,
            key='t_key',
            on_change=['1', '2']
        )

        # Mock action runners
        action1 = Mock(spec=ARunner)
        action2 = Mock(spec=ARunner)

        # Create and run observer job
        job = RedisStrObserverJob(obs, [action1, action2])
        await job.observe()

        # Assert calls to redis service
        assert m_str_get.call_count == 2
        m_str_set.assert_called_once_with(f'{ obs.key }.last', 'new_value')

        # Assert actions invoked with correct context
        expected_ctx = {
            'redis_key_old_value': 'old_value',
            'redis_key_value': 'new_value'
        }
        action1.run.assert_called_once_with(expected_ctx)
        action2.run.assert_called_once_with(expected_ctx)
