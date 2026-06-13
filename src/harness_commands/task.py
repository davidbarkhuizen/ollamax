import glob
from pathlib import Path

from chat import communicate
from config import LoomConfig
from file_utils import read_text_file_async, write_text_file_async
from harness_commands.abstract import AbstractSystemCommand
from model import CommunicationResponse


class TaskCommand(AbstractSystemCommand):
    @property
    def command(self) -> str:
        return "task"

    async def execute(self, args: list[str]) -> list[str]:
        if len(args) == 0:
            return ["error, no task specified. usage is: task [task-name], e.g. task test"]

        task = args[0]

        config: LoomConfig = self.config()

        task_folder: Path = Path(config.task.folder) / Path(task)
        task_inputs_folder: Path = task_folder / "input"

        system_text: str = await read_text_file_async(task_inputs_folder / "system.txt")
        user_text: str = await read_text_file_async(task_inputs_folder / "user.txt")

        async def context_file_block_for_files(file_paths: list[str]) -> str:
            context = []
            for path in file_paths:
                file_contents = await read_text_file_async(Path(path))
                context.append(
                    f"\n--- Begin File: {path} ---\n```python\n{file_contents}\n```\n--- End File: {path} ---\n"
                )
            return "\n".join(context)

        task_file_inputs_folder: Path = task_inputs_folder / "files"
        glob_expression = f"{task_file_inputs_folder.absolute()}/**/*.*"

        context_file_block = await context_file_block_for_files(glob.glob(glob_expression, recursive=True))

        print("!" * 80)
        print(glob_expression)
        print(context_file_block)
        print("!" * 80)

        structured_user_text: str = f"""
        context files:

        {context_file_block}

        {user_text}
"""

        response: CommunicationResponse = await communicate(
            client=self.client(),
            model=config.model.model,
            system=system_text,
            user=[structured_user_text],
            think=config.model.think,
        )

        task_outputs_folder: Path = task_folder / "output"

        await write_text_file_async(task_outputs_folder / "content.txt", response.content)

        if response.thinking:
            await write_text_file_async(task_outputs_folder / "thinking.txt", response.thinking)

        # TODO stats

        return []
