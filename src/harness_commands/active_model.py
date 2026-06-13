from rich.markdown import Markdown

from common.markdown_utils import display_markdown
from harness_commands.abstract import AbstractHarnessCommand


class ActiveModelCommand(AbstractHarnessCommand):
    @property
    def command(self) -> str:
        return "active-model"

    async def execute(self, args: list[str]) -> None:
        display_markdown(Markdown(f"{self.config().model.model}"))
