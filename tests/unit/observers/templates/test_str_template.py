from central.observers.templates.str_template import StrTemplate

class TestStrTemplate:

    def test_render_no_params(self):
        t = StrTemplate('Hello, world!')
        assert t.render() == 'Hello, world!'

    def test_render_single_argument(self):
        t = StrTemplate('Hello, {{ name }}!')
        assert t.render(name='Alice') == 'Hello, Alice!'

    def test_render_multiple_arguments(self):
        t = StrTemplate('Hello, {{ first_name }} {{ last_name }}!')
        result = t.render(first_name='Alice', last_name='Smith')
        assert result == 'Hello, Alice Smith!'

    def test_render_missing_argument(self):
        t = StrTemplate('Hello, {{ name }}!')
        assert t.render() == 'Hello, !'

    def test_render_emojis(self):
        t = StrTemplate('I ❤️ Unicode {{ icon }}!')
        assert t.render(icon='🚀') == 'I ❤️ Unicode 🚀!'
