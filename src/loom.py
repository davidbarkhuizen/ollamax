from typing import Any

from ollama import AsyncClient

from config import LoomConfig, ModelConfig
from harness_commands.abstract import AbstractSystemCommand
from harness_commands.active_model import ActiveModelCommand
from harness_commands.invoke import InvokeCommand
from harness_commands.list_models import ListModelsCommand
from harness_commands.switch_model import SwitchModelCommand
from harness_commands.switch_thinking_mode import SwitchThinkingModeCommand


def new_async_client(host: str, port: int) -> AsyncClient:
    url: str = f"http://{host}:{port}"
    return AsyncClient(host=url)


SYSTEM_COMMANDS = [ListModelsCommand, SwitchModelCommand, ActiveModelCommand, SwitchThinkingModeCommand, InvokeCommand]


async def weave(config: LoomConfig):
    print(config)

    host: str = config.ollama.host
    port: int = config.ollama.port
    client: AsyncClient = new_async_client(host, port)

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

    def register_system_commands(client: AsyncClient) -> list[AbstractSystemCommand]:
        return [X(client, get_active_config, reconfigure) for X in SYSTEM_COMMANDS]

    registered_system_commands = register_system_commands(client)

    async def execute_system_command(command: str, args: list[str]) -> list[str]:
        matching_command = [cmd for cmd in registered_system_commands if cmd.command == command]
        if len(matching_command) == 0:
            return [f"unknown system command: {command}"]

        system_command = next(iter(matching_command))
        return await system_command.execute(args)

    while (invocation := input("> ").strip()) != "exit":
        if len(invocation) == 0:
            continue

        command_response: list[str] = list()
        match invocation.split(" "):
            case []:
                pass
            case [command, *args]:
                command_response = await execute_system_command(command, args)
            case _:
                pass

        for line in command_response:
            print(line)
