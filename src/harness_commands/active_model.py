from config import OllamaConfig
from harness_commands.abstract import AbstractSystemCommand


class ActiveModelCommand(AbstractSystemCommand):
    @property
    def command(self) -> str:
        return "active-model"

    async def execute(self, args: list[str]) -> list[str]:
        config: OllamaConfig = self.config()
        return [f"active model: {config.model}"]
