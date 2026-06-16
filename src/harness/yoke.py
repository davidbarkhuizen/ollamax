import traceback
from typing import Sequence

from ollama import AsyncClient
from rich.console import Console

from config import YokeConfig
from harness.commands.abstract import AbstractHarnessCommand
from harness.commands.help import HelpCommand
from harness.commands.invoke import InvokeCommand
from harness.commands.list_commands import ListCommandsCommand
from harness.commands.list_models import ListModelsCommand
from harness.commands.list_tasks import ListTasksCommand
from harness.commands.ps import PSCommand
from harness.commands.task import TaskCommand
from harness.tether import new_async_ollama_client
from markdown.display import display_text_as_markdown, new_markdown_console

HARNESS_COMMANDS: Sequence[type[AbstractHarnessCommand]] = [
    ListModelsCommand,
    InvokeCommand,
    TaskCommand,
    PSCommand,
    ListCommandsCommand,
    HelpCommand,
    ListTasksCommand,
]


async def harness_llm(client: AsyncClient, config: YokeConfig):
    console: Console = new_markdown_console()

    registered_harness_commands: Sequence[AbstractHarnessCommand] = list()

    def register_harness_commands(client: AsyncClient) -> None:
        registered_harness_commands.extend(
            [
                T_HarnessCommand(config, client, console, registered_harness_commands)
                for T_HarnessCommand in HARNESS_COMMANDS
            ]
        )

    register_harness_commands(client)

    async def execute_harness_command(command_name: str, args: list[str]) -> bool:
        matching_commands = [cmd for cmd in registered_harness_commands if cmd.command == command_name]
        if len(matching_commands) == 0:
            display_text_as_markdown(console, f"error:  **unknown harness command: {command_name}**")
            return False

        if len(matching_commands) > 1:
            raise ValueError(f"invalid harness command configuration, multiple commands found matching {command_name}")

        harness_command = matching_commands[0]

        try:
            await harness_command.execute(config.ollama.default_model, args)
        except Exception as e:
            stack_trace: str = "\n".join(traceback.format_exception(e))
            error_message: str = f"error: unhandled exception during harness command execution - {e} - {stack_trace}"
            display_text_as_markdown(console, error_message)
            return False

    await execute_harness_command("help", [])

    while (invocation := input(f"\n{config.ollama.default_model} > ").strip().lower()) not in ["exit", "quit"]:
        if len(invocation) == 0:
            continue

        match invocation.split(" "):
            case []:
                continue
            case [command, *args]:
                await execute_harness_command(command, args)


async def yoke(config: YokeConfig):
    client = new_async_ollama_client(config.ollama.host, config.ollama.port)
    try:
        await harness_llm(client, config)
    except:
        traceback.print_exc()
        raise
    finally:
        await client.close()
