from abc import ABC, abstractmethod
from typing import Any, Callable

from ollama import AsyncClient
from rich.console import Console

from config import YokeConfig


class AbstractHarnessCommand(ABC):
    def __init__(
        self,
        config: YokeConfig,
        update_setting: Callable[[str, Any], bool],
        async_client: AsyncClient,
        console: Console,
    ):
        self.config: YokeConfig = config
        self.update_setting: Callable[[str, Any], bool] = update_setting
        self.client: AsyncClient = async_client
        self.console: Console = console

    @property
    @abstractmethod
    def command(self) -> str:
        raise NotImplementedError()

    @property
    def usage(self) -> str:
        return self.command

    @abstractmethod
    async def execute(self, model: str, think: bool, args: list[str]) -> None:
        raise NotImplementedError()
