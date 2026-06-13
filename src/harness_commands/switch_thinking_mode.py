from harness_commands.abstract import AbstractHarnessCommand


class SwitchThinkingModeCommand(AbstractHarnessCommand):
    @property
    def command(self) -> str:
        return "switch-thinking-mode"

    async def execute(self, args: list[str]) -> list[str]:
        think: bool = bool(args[0])
        reconfigured: bool = self.reconfigure("think", think)
        # validate that thinking mode is valid for model
        return [f"think switched to {think}" if reconfigured else "failed to switch think"]
