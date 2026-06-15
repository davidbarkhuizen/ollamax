import traceback
from typing import Any

from ollama import AsyncClient

from chat import new_async_ollama_client
from common.markdown import display_text_as_markdown
from config import LoomConfig
from harness_commands.abstract import AbstractHarnessCommand
from harness_commands.active_model import ActiveModelCommand
from harness_commands.invoke import InvokeCommand
from harness_commands.list_models import ListModelsCommand
from harness_commands.ps import PSCommand
from harness_commands.switch_model import SwitchModelCommand
from harness_commands.switch_thinking_mode import SwitchThinkingModeCommand
from harness_commands.task import TaskCommand

HARNESS_COMMANDS = [
    ListModelsCommand,
    SwitchModelCommand,
    ActiveModelCommand,
    SwitchThinkingModeCommand,
    InvokeCommand,
    TaskCommand,
    PSCommand,
]


async def weave(client: AsyncClient, config: LoomConfig):

    _model: str = config.ollama.default_model
    _think: bool = False

    def update_setting(setting: str, value: Any) -> bool:
        nonlocal _model
        nonlocal _think

        match setting:
            case "model":
                _model = str(value)
            case "think":
                _think = value
            case _:
                return False

        return True

    def register_harness_commands(client: AsyncClient) -> list[AbstractHarnessCommand]:
        return [X(client, config, update_setting) for X in HARNESS_COMMANDS]

    registered_harness_commands = register_harness_commands(client)

    async def execute_harness_command(command: str, args: list[str]):
        matching_command = [cmd for cmd in registered_harness_commands if cmd.command == command]
        if len(matching_command) == 0:
            display_text_as_markdown(f"unknown system command: {command}")

        system_command = next(iter(matching_command))
        await system_command.execute(_model, _think, args)

    while (invocation := input(f"\n{_model} > ").strip().lower()) not in ["exit", "quit"]:
        if len(invocation) == 0:
            continue

        match invocation.split(" "):
            case []:
                continue
            case [command, *args]:
                await execute_harness_command(command, args)
                break
            case _:
                continue


async def loom(config: LoomConfig):

    host: str = config.ollama.host
    port: int = config.ollama.port

    client = new_async_ollama_client(host, port)
    try:
        await weave(client, config)
    except:
        traceback.print_exc()
    finally:
        await client.close()
