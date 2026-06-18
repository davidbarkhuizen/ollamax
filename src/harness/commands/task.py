import glob
import json
import os
from pathlib import Path

from common.file_utils import file_is_binary, read_text_file_async, write_text_file_async
from harness.commands.abstract import AbstractHarnessCommand
from harness.tether import communicate
from markdown.display import display_text_as_markdown
from markdown.parse import extract_embedded_text_files_from_markdown
from markdown.render import dict_list_to_markdown_table, markdown_file_block_for_text_file
from model.model import CommunicationResponse, TextFile


async def context_file_block_for_text_files(text_files: list[TextFile]) -> str:

    context = []
    for text_file in text_files:
        encoded_file = markdown_file_block_for_text_file(TextFile(text_file.path, text_file.contents))
        context.extend(encoded_file.split("\n"))
        print(f"file {text_file.path} embedded into context file block")

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
        return "!"

    @property
    def usage(self) -> str:
        return f"{self.command} [task-name] [user-specification]"

    async def execute(self, model: str, args: list[str]) -> bool:

        if len(args) == 0:
            display_text_as_markdown(self.console, "error, no task specified. usage is: {self.usage}")
            return False

        task = args[0]

        task_specification_folder_path: Path = Path(self.config.folders.system) / "task" / task
        task_specification_file_path: Path = task_specification_folder_path / "system.md"

        if not os.path.exists(task_specification_file_path):
            display_text_as_markdown(self.console, f"error: **unknown task {task}**")
            return False

        if len(args) < 2:
            display_text_as_markdown(self.console, f"error: **no user specification for task**. usage is: {self.usage}")
            return False

        user_specification_name = args[1]

        user_specification_folder: Path = Path(self.config.folders.user) / user_specification_name

        display_text_as_markdown(
            self.console,
            dict_list_to_markdown_table(
                [{"task": task, "model": model, "user task specification": user_specification_name}],
                alignment="left",
                column_order=["model", "task", "user task specification"],
            ),
        )

        task_specification_text: str
        try:
            task_specification_text = await read_text_file_async(task_specification_file_path)
        except FileNotFoundError:
            display_text_as_markdown(
                self.console,
                f"error: **system prompt file for task {task} does not exist**. expected @ {task_specification_file_path}",
            )
            return False

        user_spec_text_file_path: Path = user_specification_folder / "specification.md"
        user_specification_text: str
        try:
            user_specification_text = await read_text_file_async(user_spec_text_file_path)
        except FileNotFoundError:
            display_text_as_markdown(
                self.console,
                f"error: **user specification {user_specification_name} does not exist for task {task}**",
            )
            return False

        user_spec_files_folder: Path = user_specification_folder / "files"
        user_spec_files_glob_expression = f"{user_spec_files_folder}/**/*.*"
        user_specification_files: list[TextFile] = [
            TextFile(
                path=user_spec_file_path.replace(str(user_spec_files_folder) + "/", ""),
                contents=await read_text_file_async(Path(user_spec_file_path)),
            )
            for user_spec_file_path in glob.glob(user_spec_files_glob_expression, recursive=True)
            if not await file_is_binary(user_spec_file_path)
        ]

        user_files_block = await context_file_block_for_text_files(user_specification_files)

        rsp: CommunicationResponse = await communicate(
            client=self.client,
            model=model,
            system=task_specification_text,
            user=[structured_user_text(user_files_block=user_files_block, user_text=user_specification_text)],
        )

        if rsp.stats:
            tokens_in_per_second = rsp.stats.prompt_eval_count / rsp.stats.prompt_eval_duration_s
            print(
                f"{rsp.stats.prompt_eval_count} prompt tokens evaluated in {rsp.stats.prompt_eval_duration_s:.2f} seconds => {tokens_in_per_second:.1f} tokens per second"
            )
            tokens_out_per_second = rsp.stats.eval_count / rsp.stats.eval_duration_s
            print(
                f"{rsp.stats.eval_count} tokens generated in {rsp.stats.eval_duration_s:.2f} seconds => {tokens_out_per_second:.1f} tokens per second"
            )

        thinking = rsp.thinking
        output_markdown_doc: str = rsp.content

        task_outputs_folder: Path = user_specification_folder / "generated"
        rsp_embedded_files_output_path: Path = task_outputs_folder / "files"

        if thinking:
            await write_text_file_async(task_outputs_folder / "thinking.md", rsp.thinking)

        response_text_files: list[TextFile] = extract_embedded_text_files_from_markdown(output_markdown_doc)

        os.makedirs(rsp_embedded_files_output_path, exist_ok=True)
        await write_text_file_async(task_outputs_folder / "output.md", output_markdown_doc)
        for text_file in response_text_files:
            await write_text_file_async(rsp_embedded_files_output_path / text_file.path, text_file.contents)

        print(f"extracted {len(response_text_files)} embedded text files:")
        for text_file in response_text_files:
            print(f"- {text_file.path}")

        stats_file_str: str = json.dumps(rsp.stats.__dict__, indent=4)
        await write_text_file_async(task_outputs_folder / "stats.json", stats_file_str)

        return True
