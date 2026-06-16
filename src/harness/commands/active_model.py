from rich.markdown import Markdown

from harness.commands.abstract import AbstractHarnessCommand
from markdown.display import display_markdown


class ActiveModelCommand(AbstractHarnessCommand):
    @property
    def command(self) -> str:
        return "active-model"

    async def execute(self, model: str, think: bool, args: list[str]) -> None:
        display_markdown(self.console, Markdown(f"{model}"))
