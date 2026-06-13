from dataclasses import dataclass
from enum import Enum


class ChatMessageRole(Enum):
    user = "user"
    system = "system"
    assistant = "assistant"


@dataclass
class CommunicationResponse:
    content: str
    thinking: str


@dataclass
class OllamaModel:
    name: str | None
    size_MB: int | None
    family: str | None
    format: str | None
    parameters: str | None
    quantization: str | None
