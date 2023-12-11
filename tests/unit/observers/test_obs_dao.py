from central.observers import obs_dao as dao
from central.observers.errors import (
    ActionsSectionInvalid,
    ActionsSectionNotFound,
    ActionsValidationError,
    ObserversSectionInvalid,
    ObserversSectionNotFound,
    ObserversValidationError,
)
from central.observers.models import (
    RedisListRPushAction,
    RenderTemplateAction,
)
from central.observers.obs_dao import InMemoryStore
from central.utils.futils import PathIsntFileError
from unittest.mock import patch
import pytest


class TestInMemoryStore:
    def setup_method(self, method):
        # Reset data store for every test method
        dao._dstore = InMemoryStore()

    def test_store_empty_upon_instantiation(self):
        store = InMemoryStore()
        assert not store.observers

    @patch('central.observers.obs_dao.cfg.ct_config_file')
    def test_non_existent_yaml(self, m_ct_cfg_file):
        m_ct_cfg_file.return_value = 'non_existent_yaml'
        assert not dao._dstore.initialized

        # Assert dao.all raises error during store init
        with pytest.raises(PathIsntFileError):
            dao.all()

        m_ct_cfg_file.assert_called_once()
        assert not dao._dstore.initialized

    @patch('central.observers.obs_dao.cfg.ct_config_file')
    def test_cfg_obs_section_not_found(self, mock_cfg_file):
        mock_cfg_file.return_value = 'tests/data/cfg_obs.obs_not_found.yaml'
        observers = dao.all()

        mock_cfg_file.assert_called_once()
        assert dao._dstore.initialized
        assert not observers

    @patch('central.observers.obs_dao.cfg.ct_config_file')
    def test_cfg_obs_section_not_a_list(self, mock_cfg_file):
        mock_cfg_file.return_value = 'tests/data/cfg_obs.obs_not_a_list.yaml'
        with pytest.raises(ObserversSectionInvalid):
            dao.all()

        mock_cfg_file.assert_called_once()
        assert not dao._dstore.initialized

    @patch('central.observers.obs_dao.cfg.ct_config_file')
    def test_cfg_obs_section_empty(self, mock_cfg_file):
        mock_cfg_file.return_value = 'tests/data/cfg_obs.obs_empty.yaml'
        observers = dao.all()

        assert dao._dstore.initialized
        assert not observers

    @patch('central.observers.obs_dao.cfg.ct_config_file')
    def test_cfg_obs_model_invalid(self, mock_cfg_file):
        mock_cfg_file.return_value = 'tests/data/cfg_obs.obs_model_invalid.yaml'
        with pytest.raises(ObserversValidationError):
            dao.all()

        mock_cfg_file.assert_called_once()
        assert not dao._dstore.initialized

    @patch('central.observers.obs_dao.cfg.ct_config_file')
    def test_cfg_act_model_invalid(self, mock_cfg_file):
        mock_cfg_file.return_value = 'tests/data/cfg_obs.act_model_invalid.yaml'
        with pytest.raises(ObserversValidationError):
            dao.all()

        mock_cfg_file.assert_called_once()
        assert not dao._dstore.initialized

    @patch('central.observers.obs_dao.cfg.ct_config_file')
    def test_cfg_obs_valid(self, mock_cfg_file):
        pass
