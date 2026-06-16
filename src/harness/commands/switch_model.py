from harness.commands.abstract import AbstractHarnessCommand
from markdown.display import display_text_as_markdown


class SwitchModelCommand(AbstractHarnessCommand):
    @property
    def command(self) -> str:
        return "switch-model"

    @property
    def usage(self) -> str:
        return f"{self.command} [model]"

    async def execute(self, model: str, think: bool, args: list[str]) -> None:
        new_model: str = args[0]
        reconfigured: bool = self.update_setting("model", new_model)

        if not reconfigured:
            display_text_as_markdown(self.console, "failed to switch model")
