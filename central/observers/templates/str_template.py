from jinja2 import Template as JTemplate
from .base import Template


class StrTemplate(Template):

    def __init__(self, template: str):
        self.template = template

    def render(self, **template_ctx) -> str:
        jinja_template = JTemplate(self.template)
        return jinja_template.render(**template_ctx)
