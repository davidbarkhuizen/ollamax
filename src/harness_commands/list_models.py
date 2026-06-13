from typing import Any

from ollama._types import ListResponse, ModelDetails

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

    async def execute(self, args: list[str]) -> list[str]:
        list_response: ListResponse = await self.client().list()

        ollama_models: list[OllamaModel] = [
            ollama_model_from_list_models_response_model(list_model) for list_model in list_response.models
        ]

        return [
            f"{model.family:10} {model.name:20} {model.format}, {model.parameters:5} params, {model.quantization} quantization, {model.size_MB // 1024 if model.size_MB is not None else '?'} MB"
            for model in ollama_models
        ]
