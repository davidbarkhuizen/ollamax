import pprint

from ollama._types import ProcessResponse

from harness_commands.abstract import AbstractHarnessCommand


class PSCommand(AbstractHarnessCommand):
    @property
    def command(self) -> str:
        return "ps"

    async def execute(self, args: list[str]) -> list[str]:

        response: ProcessResponse = await self.client()._request(ProcessResponse, "GET", "/api/ps")
        active_models = [model.__dict__ for model in response.models]

        lines: list[str] = list()

        for active_model in active_models:
            lines.append(pprint.pformat(active_model, indent=4, width=80))

        # print(lines)

        return lines
