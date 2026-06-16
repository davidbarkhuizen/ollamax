from harness.commands.abstract import AbstractHarnessCommand
from markdown.display import display_text_as_markdown


class SwitchThinkingModeCommand(AbstractHarnessCommand):
    @property
    def command(self) -> str:
        return "think"

    @property
    def usage(self) -> str:
        return f"{self.command} [true | false]"

    async def execute(self, model: str, think: bool, args: list[str]) -> None:
        new_think: bool = bool(args[0])
        updated: bool = self.update_setting("think", new_think)
        # validate that thinking mode is supported by model
        display_text_as_markdown(f"thinking-mode switched to {new_think}" if updated else "failed to switch think-mode")
