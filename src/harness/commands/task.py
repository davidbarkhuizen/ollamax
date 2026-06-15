import glob
import os
from pathlib import Path

from common.file_utils import read_text_file_async, write_text_file_async
from common.markdown import display_text_as_markdown, extract_embedded_files_from_markdown
from harness.commands.abstract import AbstractHarnessCommand
from harness.tether import communicate
from model.model import CommunicationResponse


async def context_file_block_from_files(file_paths: list[str]) -> str:
    context = []
    for path in file_paths:
        file_contents = await read_text_file_async(Path(path))
        context.append(f"\n--- Begin File: {path} ---\n```python\n{file_contents}\n```\n--- End File: {path} ---\n")
    return "\n".join(context)


def structured_user_text(user_files_block, user_text) -> str:

    return f"""
# user prompt

## files

{user_files_block}

## specification

{user_text}
"""


class TaskCommand(AbstractHarnessCommand):
    @property
    def command(self) -> str:
        return "task"

    @property
    def usage(self) -> str:
        return f"{self.command} [task-name] [task-specification]"

    async def execute(self, model: str, think: bool, args: list[str]) -> None:

        if len(args) == 0:
            display_text_as_markdown(f"error, no task specified. usage is: {self.usage}")
        task = args[0]

        if len(args) < 2:
            display_text_as_markdown(f"error, no task specification specified. usage is: {self.usage}")
        specification = args[1]

        system_inputs_folder: Path = Path(self.config.folders.system) / "task" / task
        user_inputs_folder: Path = Path(self.config.folders.user) / specification
        user_input_files_folder: Path = user_inputs_folder / "files"
        glob_expression = f"{user_input_files_folder.absolute()}/**/*.*"

        task_outputs_folder: Path = Path(self.config.folders.generated) / specification
        rsp_embedded_files_output_path: Path = task_outputs_folder / "files"

        system_text: str = await read_text_file_async(system_inputs_folder / "system.md")
        user_text: str = await read_text_file_async(user_inputs_folder / "specification.md")
        user_files_block = await context_file_block_from_files(glob.glob(glob_expression, recursive=True))

        display_text_as_markdown(f"{model}: {task} {specification}")
        rsp: CommunicationResponse = await communicate(
            client=self.client,
            model=model,
            system=system_text,
            user=[structured_user_text(user_files_block=user_files_block, user_text=user_text)],
            think=think,
        )

        thinking = rsp.thinking
        output_markdown_doc: str = rsp.content
        rsp_embedded_files: list[tuple[str, str]] = extract_embedded_files_from_markdown(output_markdown_doc)

        os.makedirs(rsp_embedded_files_output_path, exist_ok=True)
        if thinking:
            await write_text_file_async(task_outputs_folder / "thinking.md", rsp.thinking)
        await write_text_file_async(task_outputs_folder / "output.md", output_markdown_doc)
        for file_contents, relative_file_path in rsp_embedded_files:
            await write_text_file_async(rsp_embedded_files_output_path / relative_file_path, file_contents)

        # TODO stats
