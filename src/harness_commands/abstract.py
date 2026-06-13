from abc import ABC, abstractmethod
from typing import Any, Callable

from ollama import AsyncClient

from config import LoomConfig


class AbstractSystemCommand(ABC):
    def __init__(
        self, async_client: AsyncClient, get_config: Callable[[], LoomConfig], reconfigure: Callable[[str, Any], bool]
    ):
        self._async_client: AsyncClient = async_client
        self._get_config: Callable[[], LoomConfig] = get_config
        self._reconfigure: Callable[[str, Any], bool] = reconfigure

    def client(self) -> AsyncClient:
        return self._async_client

    def config(self) -> LoomConfig:
        return self._get_config()

    def reconfigure(self, setting: str, value: Any) -> bool:
        return self._reconfigure(setting, value)

    @property
    @abstractmethod
    def command(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    async def execute(self, args: list[str]) -> list[str]:
        raise NotImplementedError()
