import glob
import os
from pathlib import Path

from common.file_utils import file_is_binary, read_text_file_async, write_text_file_async
from harness.commands.abstract import AbstractHarnessCommand
from harness.tether import communicate
from markdown.display import display_text_as_markdown
from markdown.parse import extract_embedded_files_from_markdown
from model.model import CommunicationResponse

CSV = "csv"
PYTHON = "python"
SQL = "sql"
TEXT = "text"


language_for_file_extension: dict[str, str] = {".py": PYTHON, ".txt": TEXT, ".sql": SQL, ".csv": CSV}


async def context_file_block_from_file_paths(file_paths: list[str]) -> str:

    processed_file_count: int = 0
    embedded_file_count: int = 0
    binary_file_count: int = 0

    context = []
    for path in file_paths:
        try:
            processed_file_count = processed_file_count + 1
            if await file_is_binary(path):
                binary_file_count = binary_file_count + 1
                continue
            file_contents = await read_text_file_async(Path(path))

            # determine lang marker from file extension
            #
            lang: str = "text"
            for file_ext in language_for_file_extension.keys():
                if path.endswith(file_ext):
                    lang = language_for_file_extension[file_ext]
                    break

            encoded_file = f"""

**`{path}`**
```{lang}
{file_contents}
```

"""

            context.extend(encoded_file.split("\n"))
            embedded_file_count = embedded_file_count + 1
            print(f"file {path} embedded into context file block")
        except:
            print(f"error reading file @ {path}")
            raise

    print(
        f"processed {processed_file_count} files, embedded {embedded_file_count}, ignored {binary_file_count} binary files"
    )

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

        system_text: str = await read_text_file_async(system_inputs_folder / "system.md")
        user_text: str = await read_text_file_async(user_inputs_folder / "specification.md")
        user_files_block = await context_file_block_from_file_paths(glob.glob(glob_expression, recursive=True))

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

        task_outputs_folder: Path = Path(self.config.folders.generated) / specification
        rsp_embedded_files_output_path: Path = task_outputs_folder / "files"

        if thinking:
            await write_text_file_async(task_outputs_folder / "thinking.md", rsp.thinking)

        rsp_embedded_files: list[tuple[str, str]] = extract_embedded_files_from_markdown(output_markdown_doc)
        print(f"response contains {len(rsp_embedded_files)} embedded files")

        os.makedirs(rsp_embedded_files_output_path, exist_ok=True)
        await write_text_file_async(task_outputs_folder / "output.md", output_markdown_doc)
        for file_contents, relative_file_path in rsp_embedded_files:
            await write_text_file_async(rsp_embedded_files_output_path / relative_file_path, file_contents)

        # TODO stats
