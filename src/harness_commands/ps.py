from ollama._types import ProcessResponse

from common.markdown_utils import dicts_to_markdown_table, display_markdown
from harness_commands.abstract import AbstractHarnessCommand


class PSCommand(AbstractHarnessCommand):
    @property
    def command(self) -> str:
        return "ps"

    async def execute(self, args: list[str]) -> None:

        response: ProcessResponse = await self.client()._request(ProcessResponse, "GET", "/api/ps")

        FIELDS_TO_EXCLUDE = [
            "modified_at",
            "parent_model",
            "families",
            "digest",
            "family",
            "format",
            "expires_at",
        ]

        model_dicts = [
            {k: v for k, v in model.__dict__.items() if k not in FIELDS_TO_EXCLUDE} for model in response.models
        ]

        for model_dict in model_dicts:
            model_dict["size"] = f"{int(model_dict['size']) // (1024 * 1024 * 1024)} GB"
            details_object = model_dict.pop("details")
            details = {k: v for k, v in details_object.__dict__.items() if k not in FIELDS_TO_EXCLUDE}
            model_dict.update(details)

        model_dicts = sorted(model_dicts, key=lambda d: d["model"])
        display_markdown(dicts_to_markdown_table(model_dicts))
