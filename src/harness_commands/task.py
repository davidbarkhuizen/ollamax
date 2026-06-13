import os

from chat import communicate
from config import LoomConfig
from file_utils import read_text_file_async
from harness_commands.abstract import AbstractSystemCommand


async def load_task_specification_from_file(file_path: str) -> str:
    return await read_text_file_async(file_path)


class TaskCommand(AbstractSystemCommand):
    @property
    def command(self) -> str:
        return "task"

    async def execute(self, args: list[str]) -> list[str]:

        config: LoomConfig = self.config()

        task_file_path = os.path.join(config.task.folder, config.task.specification_file_name)

        task_specification: str = await load_task_specification_from_file(task_file_path)

        response_lines: list[str] = await communicate(
            client=self.client(),
            model=config.model.model,
            role="user",
            text=task_specification,
            think=config.model.think,
        )

        return response_lines
