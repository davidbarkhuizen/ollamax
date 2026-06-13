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
