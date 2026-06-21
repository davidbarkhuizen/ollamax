from typing_extensions import Any, Callable

from harness.commands.abstract import AbstractHarnessCommand
from harness.tether import prompt
from harness.tool_logic import call_tool
from harness.tools.tools.maths.arithmetic import add, divide, multiply, subtract
from harness.tools.tools.temporal.time import get_current_date_time, get_day_of_week
from model.model import RawPromptRequest, RawPromptResponse


class QueryCommand(AbstractHarnessCommand):
    @property
    def command(self) -> str:
        return "?"

    @property
    def usage(self) -> str:
        return "? [natural language query]"

    async def execute(self, model: str, args: list[str]) -> bool:

        text = " ".join(args)

        available_tools: list[Callable] = [get_current_date_time, get_day_of_week, add, subtract, divide, multiply]

        initial_rq = RawPromptRequest(system_prompt="", user_prompt=[text], tools=available_tools, message_history=[])
        initial_rsp: RawPromptResponse = await prompt(self.client, model, initial_rq)

        message_history: list[dict[str, Any]] = list(initial_rsp.message_history)

        tool_calls = initial_rsp.tool_calls
        while len(tool_calls) > 0:
            tool_call_response_messages = []

            for tool_call in tool_calls:
                tool_call_response_message: dict[str, str] = await call_tool(self.console, available_tools, tool_call)
                tool_call_response_messages.append(tool_call_response_message)

            message_history.extend(tool_call_response_messages)

            rsp: RawPromptResponse = await prompt(
                self.client,
                model,
                RawPromptRequest(
                    system_prompt="", user_prompt=[], tools=available_tools, message_history=message_history
                ),
            )
            tool_calls = [*rsp.tool_calls]
            message_history = rsp.message_history

        return True
