import aiofiles
import logging
from pydantic.networks import FileUrl
from typing import Any, Dict
from ..models import RenderTemplateAction
from ..templates.str_template import StrTemplate
from .base import ARunner
from central.utils import futils


logger = logging.getLogger(__name__)


class RenderTemplateRunner(ARunner):

    def __init__(self, action: RenderTemplateAction):
        self.action = action

    async def run(self, context: Dict[str, Any]) -> None:
        logger.info(f'Running render_template action: { self.action.name }')

        template = await self._load_template(self.action.template_uri.path)
        render_output = StrTemplate(template).render(**context)
        await self._write_render_output(render_output)

    async def _load_template(self, template_path: str) -> str:
        futils.verify_file_existence(template_path)

        async with aiofiles.open(template_path, mode='r') as f:
            template = await f.read()
        return template

    async def _write_render_output(self, render_output: str) -> None:
        async with aiofiles.open(self.action.output_uri.path, mode='w') as f:
            await f.write(render_output)
