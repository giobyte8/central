from central.observers.configstores.yaml import YamlConfigStore
from central.observers.errors import (
    ActionNotFoundError,
    ObserversInvalidConfigError,
)
from unittest.mock import patch
import pytest


class TestYamlConfigStore:

    @patch('central.observers.configstores.yaml.cfg.ct_config_file')
    def test_load_valid_config(self, ct_config_file):
        ct_config_file.return_value = 'tests/data/cfg.obs.valid.yaml'
        store = YamlConfigStore()

        assert 2 == len(store.get_observers())
        assert 5 == len(store._actions)

    @patch('central.observers.configstores.yaml.cfg.ct_config_file')
    def test_load_obs_empty(self, ct_config_file):
        ct_config_file.return_value = 'tests/data/cfg.obs.empty.yaml'
        with pytest.raises(ObserversInvalidConfigError):
            YamlConfigStore()

    @patch('central.observers.configstores.yaml.cfg.ct_config_file')
    def test_load_obs_missing_attrs(self, ct_config_file):
        ct_config_file.return_value = 'tests/data/cfg.obs.missing_attrs.yaml'

        with pytest.raises(ValueError):
            YamlConfigStore()

    @patch('central.observers.configstores.yaml.cfg.ct_config_file')
    def test_load_obs_not_a_list(self, ct_config_file):
        ct_config_file.return_value = 'tests/data/cfg.obs.not_a_list.yaml'
        with pytest.raises(ObserversInvalidConfigError):
            YamlConfigStore()

    @patch('central.observers.configstores.yaml.cfg.ct_config_file')
    def test_load_non_existent_action(self, ct_config_file):
        ct_config_file.return_value = 'tests/data/cfg.obs.non_existent_action.yaml'
        with pytest.raises(ActionNotFoundError):
            YamlConfigStore()

