from common.markdown_utils import display_text_as_markdown
from harness_commands.abstract import AbstractHarnessCommand


class SwitchThinkingModeCommand(AbstractHarnessCommand):
    @property
    def command(self) -> str:
        return "switch-thinking-mode"

    async def execute(self, args: list[str]) -> None:
        think: bool = bool(args[0])
        reconfigured: bool = self.reconfigure("think", think)
        # validate that thinking mode is valid for model
        display_text_as_markdown(f"think switched to {think}" if reconfigured else "failed to switch think")
