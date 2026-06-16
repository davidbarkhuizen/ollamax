from ollama._types import ListResponse

from harness.commands.abstract import AbstractHarnessCommand
from markdown.display import display_markdown
from markdown.render import dicts_to_markdown_table


class ListModelsCommand(AbstractHarnessCommand):
    @property
    def command(self) -> str:
        return "list-models"

    async def execute(self, model: str, think: bool, args: list[str]) -> None:
        response: ListResponse = await self.client.list()

        FIELDS_TO_EXCLUDE = ["modified_at", "parent_model", "families", "digest"]

        model_dicts = [
            {k: v for k, v in model.__dict__.items() if k not in FIELDS_TO_EXCLUDE} for model in response.models
        ]

        for model_dict in model_dicts:
            model_dict["size"] = f"{str(int(model_dict['size']) // (1024 * 1024 * 1024)).ljust(3, ' ')} GB"
            model_details_object = model_dict.pop("details")
            model_details_dict = {k: v for k, v in model_details_object.__dict__.items() if k not in FIELDS_TO_EXCLUDE}
            model_dict.update(model_details_dict)

        model_dicts = sorted(model_dicts, key=lambda d: d["model"])
        display_markdown(self.console, dicts_to_markdown_table(model_dicts))
