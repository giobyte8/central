import pytest
from pydantic import ValidationError
from central.observers.models import (
    RedisListRPushAction,
    RenderTemplateAction,
)


class TestRedisListRPushAction:

    def test_load_missing_field(self):
        data = {
            'name': 'rlrp_test',
            'list_key': 'random_test_key'
        }

        # Missing required field 'msg_templates'
        with pytest.raises(ValidationError):
            _ = RedisListRPushAction(**data)

    def test_load(self):
        data = {
            'name': 'rlrp_test',
            'list_key': 'random_test_key',
            'msg_template': 'test_template',
        }

        action = RedisListRPushAction(**data)
        assert action.name == 'rlrp_test'
        assert action.list_key == 'random_test_key'
        assert action.msg_template == 'test_template'


class TestRenderTemplateAction:
    def test_load_invalid_template_path(self):
        data = {
            'name': 'rt_test',
            'template_path': 'relative/invalid_path/template',
            'output_path': 'file:///abs/path/file.html'
        }

        # Invalid template path
        with pytest.raises(ValidationError):
            _ = RenderTemplateAction(**data)


    def test_load_invalid_output_path(self):
        data = {
            'name': 'rt_test',
            'template_path': 'file://relative/path/template',
            'output_path': './INVALID/path/file.html'
        }

        # Invalid template path
        with pytest.raises(ValidationError):
            _ = RenderTemplateAction(**data)


    ## Load a valid action
    def test_load(self):
        data = {
            'name': 'rt_test',
            'template_path': 'file://relative/path/template',
            'output_path': 'file:///abs/path/file.html'
        }

        action = RenderTemplateAction(**data)
        assert action.name == 'rt_test'
        assert str(action.template_path) == 'file://relative/path/template'
        assert str(action.output_path) == 'file:///abs/path/file.html'


class TestRedisStringObserver:
    pass


class TestHttpStatusObserver:
    pass
