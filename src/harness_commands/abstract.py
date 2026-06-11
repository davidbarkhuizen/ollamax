from abc import ABC, abstractmethod

from ollama import AsyncClient


class AbstractHarnessCommand(ABC):
    def __init__(self, async_client: AsyncClient):
        self.async_client: AsyncClient = async_client

    def client(self) -> AsyncClient:
        return self.async_client

    @property
    @abstractmethod
    def command(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    async def execute(self, args: list[str]) -> list[str]:
        raise NotImplementedError()
