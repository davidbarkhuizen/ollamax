import asyncio

from config import Config, configure_from_json_file
from loom import weave

if __name__ == "__main__":
    config: Config = configure_from_json_file()
    print(config)

    asyncio.run(weave(config.ollama.host, config.ollama.port, config.ollama.model))
