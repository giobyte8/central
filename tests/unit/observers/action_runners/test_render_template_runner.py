import os
import pytest
from central.observers.action_runners.render_template_runner import (
    RenderTemplateRunner
)
from central.observers.models import RenderTemplateAction
from central.utils.futils import PathIsNotAFileError


class TestRenderTemplateAction:

    @pytest.mark.asyncio
    async def test_non_existent_template(self):
        non_existent_path = 'file:///tests/templates/non_existent.template'
        action = RenderTemplateAction(
            name='test',
            template_uri=non_existent_path,
            output_uri='file:///tests/templates/non_existent.txt'
        )
        action_runner = RenderTemplateRunner(action)

        with pytest.raises(PathIsNotAFileError):
            await action_runner.run(context={})

    @pytest.mark.asyncio
    async def test_no_variables_template(self):
        t_rel_path = 'tests/templates/no_variables.template'
        t_abs_path = os.path.abspath(t_rel_path)
        template_uri = 'file://{}'.format(t_abs_path)

        output_rel_path = 'tests/templates/no_variables.txt'
        output_abs_path = os.path.abspath(output_rel_path)
        output_uri = 'file://{}'.format(output_abs_path)

        action = RenderTemplateAction(
            name='test',
            template_uri=template_uri,
            output_uri=output_uri
        )
        action_runner = RenderTemplateRunner(action)

        await action_runner.run(context={'foo': 'bar'})

        with open(output_abs_path, 'r') as f:
            assert f.read() == '<h1>A template without variables</h1>'


    @pytest.mark.asyncio
    async def test_with_context_template(self):
        t_rel_path = 'tests/templates/temperature.template'
        t_abs_path = os.path.abspath(t_rel_path)
        template_uri = 'file://{}'.format(t_abs_path)

        output_rel_path = 'tests/templates/temperature.html'
        output_abs_path = os.path.abspath(output_rel_path)
        output_uri = 'file://{}'.format(output_abs_path)

        action = RenderTemplateAction(
            name='test_temperature',
            template_uri=template_uri,
            output_uri=output_uri
        )
        action_runner = RenderTemplateRunner(action)

        await action_runner.run(context={
            'name': 'John Doe',
            'celsius_temp': 22
        })

        # Verify rendered content
        with open(output_abs_path, 'r') as f:
            assert f.read() == (
                '<h1>Hello John Doe</h1>\n'
                '<p>Current temperature is 22 celsius</p>'
            )
