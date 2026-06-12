from harness_commands.abstract import AbstractSystemCommand


class SwitchModelCommand(AbstractSystemCommand):
    @property
    def command(self) -> str:
        return "switch-model"

    async def execute(self, args: list[str]) -> list[str]:
        model: str = args[0]
        reconfigured: bool = self.reconfigure("model", model)
        return [f"switched to model {model}" if reconfigured else "failed to switch model"]
