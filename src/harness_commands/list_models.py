from ollama._types import ListResponse, ModelDetails

from common.markdown_utils import dicts_to_markdown_table, display_markdown
from harness_commands.abstract import AbstractHarnessCommand
from model import OllamaModel


def ollama_model_from_list_models_response_model(model: ListResponse.Model) -> OllamaModel:

    details: ModelDetails | None = model.details

    return OllamaModel(
        name=model.model if model.model else None,
        size_MB=model.size // (1024 * 1024) if model.size else 0,
        family=details.family if details else None,
        format=details.format if details else None,
        parameters=details.parameter_size if details and details.parameter_size else None,
        quantization=details.quantization_level if details else None,
    )


class ListModelsCommand(AbstractHarnessCommand):
    @property
    def command(self) -> str:
        return "list-models"

    async def execute(self, args: list[str]) -> None:
        list_response: ListResponse = await self.client().list()

        models: list[OllamaModel] = [
            ollama_model_from_list_models_response_model(list_model) for list_model in list_response.models
        ]

        display_markdown(dicts_to_markdown_table([model.__dict__ for model in models]))
