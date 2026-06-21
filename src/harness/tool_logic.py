from typing import Any, Callable, Mapping

from ollama import Message

from harness.tether import new_message
from markdown.display import display_text_as_markdown
from markdown.render import dict_list_to_markdown_table


async def call_tool(console, tools: list[Callable], tool_call: Message.ToolCall) -> dict[str, str]:

    target_tool_name: str = tool_call.function.name
    tool_call_arguments: Mapping[str, Any] = tool_call.function.arguments

    display_text_as_markdown(console, f"tool: **{target_tool_name}**")
    if len(tool_call_arguments.keys()) > 0:
        display_text_as_markdown(console, dict_list_to_markdown_table([tool_call_arguments]))

    tool_fn: Callable = [tool for tool in tools if tool.__name__ == target_tool_name][0]
    tool_call_result: str = await tool_fn(**tool_call_arguments)

    display_text_as_markdown(console, f"result: {tool_call_result}")

    return new_message(role="tool", tool_name=target_tool_name, text=tool_call_result)
