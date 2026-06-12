from harness_commands.abstract import AbstractSystemCommand


class ListModelsCommand(AbstractSystemCommand):
    @property
    def command(self) -> str:
        return "list-models"

    async def execute(self, args: list[str]) -> list[str]:
        ollama_rsp = await self.client().list()
        models = [model.__dict__ for model in ollama_rsp["models"]]

        lines: list[str] = []
        for model in models:
            model_name = model["model"]
            model_size_GB = model["size"] // (1024 * 1024 * 1024)

            details = model["details"]
            family = details["family"]
            format = details["format"]
            parameter_size = details["parameter_size"]
            quantization = details["quantization_level"]

            lines.append(
                f"{family:10} {model_name:20} {format}, {parameter_size:5} params, {quantization} quantization, {model_size_GB} GB"
            )

        return lines
