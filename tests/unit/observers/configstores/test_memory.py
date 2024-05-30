import pytest
from central.observers.configstores.memory import MemoryConfigStore
from central.observers.errors import ConfigStoreError
from central.observers.models import (
    RedisStringObserver,
    RedisListRPushAction
)


def make_observer(name: str) -> RedisStringObserver:
    return RedisStringObserver(
        name=name,
        interval=5,
        key='test_string',
        on_change=['action1', 'action2']
    )


def make_action(name: str) -> RedisListRPushAction:
    return RedisListRPushAction(
        name=name,
        list_key='test_list',
        msg_template='A random template'
    )


class TestMemoryConfigStore:
    def test_add_observers(self) -> None:
        o = make_observer('test_observer')
        store = MemoryConfigStore()
        store.add_observer(o)

        assert o in store.get_observers()

    def test_add_duplicated_observer(self) -> None:
        o = make_observer('ipv4_observer')
        store = MemoryConfigStore()
        store.add_observer(o)

        # Adding observer with same name, raises error
        observer2 = make_observer('ipv4_observer')
        with pytest.raises(ConfigStoreError):
            store.add_observer(observer2)


    def test_add_actions(self) -> None:
        a1 = make_action('action1')
        a2 = make_action('action2')

        store = MemoryConfigStore()
        store.add_actions([a1, a2])
        assert a1 == store.find_action('action1')
        assert a2 == store.find_action('action2')

    def test_add_duplicated_action(self) -> None:
        action_1 = make_action('stop_galleries')
        action_2 = make_action('stop_galleries')

        with pytest.raises(ConfigStoreError):
            MemoryConfigStore().add_actions([action_1, action_2])

    def test_find_unexistent_action(self) -> None:
        action1 = make_action('action1')

        store = MemoryConfigStore()
        store.add_actions([action1])
        assert not store.find_action('unexistent_action')

    def test_action_exists(self) -> None:
        action1 = make_action('action1')

        store = MemoryConfigStore()
        store.add_actions([action1])
        assert store.action_exists('action1')
        assert not store.action_exists('unexistent_action')
