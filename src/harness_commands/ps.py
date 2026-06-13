from ollama._types import ProcessResponse

from common.markdown_utils import dicts_to_markdown_table, display_markdown
from harness_commands.abstract import AbstractHarnessCommand


class PSCommand(AbstractHarnessCommand):
    @property
    def command(self) -> str:
        return "ps"

    async def execute(self, args: list[str]) -> None:

        response: ProcessResponse = await self.client()._request(ProcessResponse, "GET", "/api/ps")
        models = [model.__dict__ for model in response.models]
        display_markdown(dicts_to_markdown_table([model.__dict__ for model in models]))
