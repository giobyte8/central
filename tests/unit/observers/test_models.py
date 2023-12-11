import pytest
from pydantic import ValidationError
from central.observers.models import (
    RedisListRPushAction,
    RenderTemplateAction,
    DockerCtrStartAction,
    RedisStringObserver,
    HttpStatusRequest,
    HttpStatusObserver,
)


class TestRedisListRPushAction:

    def test_load_missing_field(self):
        data = {
            'name': 'rlrp_test',
            'action_type': 'redis_list_rpush',
            'list_key': 'random_test_key',
            # 'msg_template' is missing
        }

        with pytest.raises(ValidationError) as e:
            _ = RedisListRPushAction(**data)

        # Original error is contained inside pytest ExceptionInfo.value
        e = e.value
        assert e.error_count() == 1
        assert e.errors()[0]['loc'] == ('msg_template',)
        assert e.errors()[0]['type'] == 'missing'

    def test_load(self):
        data = {
            'name': 'rlrp_test',
            'action_type': 'redis_list_rpush',
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
            'action_type': 'render_template',
            'template_path': 'relative/invalid_path/template',
            'output_path': 'file:///abs/path/file.html'
        }

        with pytest.raises(ValidationError) as e:
            _ = RenderTemplateAction(**data)

        # Original error is contained inside pytest ExceptionInfo.value
        e = e.value
        assert e.error_count() == 1
        assert e.errors()[0]['loc'] == ('template_path',)
        assert e.errors()[0]['type'] == 'url_parsing'

    def test_load_invalid_output_path(self):
        data = {
            'name': 'rt_test',
            'action_type': 'render_template',
            'template_path': 'file://relative/path/template',
            'output_path': './INVALID/path/file.html'
        }

        with pytest.raises(ValidationError) as e:
            _ = RenderTemplateAction(**data)

        # Original error is contained inside pytest ExceptionInfo.value
        e = e.value
        assert e.error_count() == 1
        assert e.errors()[0]['loc'] == ('output_path',)
        assert e.errors()[0]['type'] == 'url_parsing'

    def test_load_wrong_type(self):
        data = {
            'name': 'rt_test',
            'action_type': 'wonrg_value',
            'template_path': 'file://relative/path/template',
            'output_path': 'file:///abs/path/file.html'
        }

        with pytest.raises(ValidationError) as e:
            _ = RenderTemplateAction(**data)

        # Original error is contained inside pytest ExceptionInfo.value
        e = e.value
        assert e.error_count() == 1
        assert e.errors()[0]['loc'] == ('action_type',)
        assert e.errors()[0]['type'] == 'literal_error'

    ## Load a valid action
    def test_load(self):
        data = {
            'name': 'rt_test',
            'action_type': 'render_template',
            'template_path': 'file://relative/path/template',
            'output_path': 'file:///abs/path/file.html'
        }

        action = RenderTemplateAction(**data)
        assert action.name == 'rt_test'
        assert str(action.template_path) == 'file://relative/path/template'
        assert str(action.output_path) == 'file:///abs/path/file.html'


class TestDockerCtrStartAction:
    def test_load_missing_name(self):
        data = {
            # 'name' is missing
            'action_type': 'docker_ctr_start',
            'container': 'test_container'
        }

        with pytest.raises(ValidationError) as e:
            _ = DockerCtrStartAction(**data)

        e = e.value
        assert e.error_count() == 1
        assert e.errors()[0]['loc'] == ('name',)
        assert e.errors()[0]['type'] == 'missing'

    def test_load(self):
        data = {
            'name': 'start_nginx',
            'action_type': 'docker_ctr_start',
            'container': 'test_container'
        }

        action = DockerCtrStartAction(**data)
        assert action.name == 'start_nginx'
        assert action.container == 'test_container'

class TestRedisStringObserver:
    def test_load_empty_actions_list(self):
        data = {
            'name': 'rso_test',
            'observer_type': 'redis_string',
            'interval': 10,
            'key': 'test_key',
            'on_change': []
        }

        with pytest.raises(ValidationError) as e:
            _ = RedisStringObserver(**data)
        assert e.value.error_count() == 1
        assert e.value.errors()[0]['loc'] == ('on_change',)
        assert e.value.errors()[0]['type'] == 'too_short'

    def test_load_non_int_interval(self):
        data = {
            'name': 'rso_test',
            'observer_type': 'redis_string',
            'interval': 10.5,
            'key': 'test_key',
            'on_change': [
                {
                    'name': 'rlrp_test',
                    'action_type': 'redis_list_rpush',
                    'list_key': 'random_test_key',
                    'msg_template': 'test_template',
                }
            ]
        }

        # Rational number raises error
        with pytest.raises(ValidationError) as e:
            _ = RedisStringObserver(**data)
        assert e.value.error_count() == 1
        assert e.value.errors()[0]['loc'] == ('interval',)
        assert e.value.errors()[0]['type'] == 'int_from_float'

        # String instead of number raises error
        data['interval'] = '10s'
        with pytest.raises(ValidationError) as e:
            _ = RedisStringObserver(**data)
        assert e.value.error_count() == 1
        assert e.value.errors()[0]['loc'] == ('interval',)
        assert e.value.errors()[0]['type'] == 'int_parsing'

    def test_load(self):
        data = {
            'name': 'rso_test',
            'observer_type': 'redis_string',
            'interval': 10,
            'key': 'test_key',
            'on_change': [
                {
                    'name': 'rlrp_test',
                    'action_type': 'redis_list_rpush',
                    'list_key': 'random_test_key',
                    'msg_template': 'test_template',
                }
            ]
        }

        observer = RedisStringObserver(**data)
        assert observer.name == 'rso_test'
        assert observer.interval == 10
        assert observer.key == 'test_key'

        assert len(observer.on_change) == 1
        assert type(observer.on_change[0]) == RedisListRPushAction
        assert observer.on_change[0].name == 'rlrp_test'
        assert observer.on_change[0].list_key == 'random_test_key'
        assert observer.on_change[0].msg_template == 'test_template'


class TestHttpStatusRequest:
    def test_load_invalid_url(self):
        data = {
            'endpoint': 'wrong_value',
            'verb': 'GET',
        }

        with pytest.raises(ValidationError) as e:
            _ = HttpStatusRequest(**data)
        assert e.value.error_count() == 1
        assert e.value.errors()[0]['loc'] == ('endpoint',)
        assert e.value.errors()[0]['type'] == 'url_parsing'

    def test_load_invalid_verb(self):
        data = {
            'endpoint': 'http://example.com',
            'verb': 'WRONG_VALUE',
        }

        with pytest.raises(ValidationError) as e:
            _ = HttpStatusRequest(**data)
        assert e.value.error_count() == 1
        assert e.value.errors()[0]['loc'] == ('verb',)
        assert e.value.errors()[0]['type'] == 'enum'


class TestHttpStatusObserver:
    pass
