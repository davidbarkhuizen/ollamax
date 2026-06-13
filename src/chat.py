from typing import Any

from ollama import AsyncClient


def new_message(role: str, text: str, think: bool) -> dict[str, Any]:
    return {"content": text, "role": role, "think": think}


async def communicate(client: AsyncClient, model: str, role: str, text: str, think: bool) -> list[str]:

    message = new_message(role, text, think)

    stream = await client.chat(model=model, messages=[message], stream=True)

    response_text: str = ""
    thinking_text: str = ""

    async for part in stream:
        with open("log.log", "a") as file:
            file.write(str(part) + "\n")

        thinking: str | None = part["message"].thinking
        if thinking:
            thinking_text += thinking
            print(thinking, end="", flush=True)

        content: str = part["message"]["content"]
        if content:
            response_text += content
            print(content, end="", flush=True)

        #     done: bool = part["done"]
        #     done_reason: str | None = part.done_reason

    return [response_text]
