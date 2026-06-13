from typing import Any

from ollama import AsyncClient

from chat import new_async_ollama_client
from config import LoomConfig, ModelConfig
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


async def weave(config: LoomConfig):
    print(config)

    host: str = config.ollama.host
    port: int = config.ollama.port
    client: AsyncClient = new_async_ollama_client(host, port)

    _model: str = config.model.model
    _think: bool = config.model.think

    def get_active_config() -> LoomConfig:
        return LoomConfig(log=config.log, model=ModelConfig(model=_model, think=_think), ollama=config.ollama)

    def reconfigure(setting: str, value: Any) -> bool:
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
        return [X(client, get_active_config, reconfigure) for X in HARNESS_COMMANDS]

    registered_harness_commands = register_harness_commands(client)

    async def execute_harness_command(command: str, args: list[str]):
        matching_command = [cmd for cmd in registered_harness_commands if cmd.command == command]
        if len(matching_command) == 0:
            return [f"unknown system command: {command}"]

        system_command = next(iter(matching_command))
        await system_command.execute(args)

    while (invocation := input("> ").strip().lower()) not in ["exit", "quit"]:
        if len(invocation) == 0:
            continue

        match invocation.split(" "):
            case []:
                continue
            case [command, *args]:
                await execute_harness_command(command, args)
            case _:
                continue
