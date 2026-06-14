from chat import communicate
from config import LoomConfig
from harness_commands.abstract import AbstractHarnessCommand
from model import CommunicationResponse


class InvokeCommand(AbstractHarnessCommand):
    @property
    def command(self) -> str:
        return "!"

    async def execute(self, args: list[str]) -> None:

        config: LoomConfig = self.config()

        text = " ".join(args)

        _: CommunicationResponse = await communicate(
            client=self.client(), model=config.model.model, system="", user=[text], think=config.model.think
        )
