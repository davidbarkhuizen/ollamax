from chat import communicate
from config import LoomConfig
from harness_commands.abstract import AbstractSystemCommand


class InvokeCommand(AbstractSystemCommand):
    @property
    def command(self) -> str:
        return "invoke"

    async def execute(self, args: list[str]) -> list[str]:

        config: LoomConfig = self.config()

        text = " ".join(args)

        response_lines: list[str] = await communicate(
            client=self.client(), model=config.model.model, role="user", text=text, think=config.model.think
        )

        return response_lines
