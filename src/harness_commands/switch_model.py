from common.markdown_utils import display_text_as_markdown
from harness_commands.abstract import AbstractHarnessCommand


class SwitchModelCommand(AbstractHarnessCommand):
    @property
    def command(self) -> str:
        return "switch-model"

    async def execute(self, args: list[str]) -> None:
        model: str = args[0]
        reconfigured: bool = self.reconfigure("model", model)

        if not reconfigured:
            display_text_as_markdown("failed to switch model")
