import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from dacite import from_dict
from dacite.config import Config

CONFIG_FILE_PATH = "./loom.config.json"


@dataclass
class LogConfig:
    root_folder: str = field(default_factory=lambda: "log")


@dataclass
class TasksConfig:
    folder: str = field(default_factory=lambda: "tasks")


@dataclass
class ModelConfig:
    model: str
    think: bool


@dataclass
class OllamaConfig:
    host: str = field(default_factory=lambda: "localhost")
    port: int = field(default_factory=lambda: 11434)


@dataclass
class LoomConfig:
    model: ModelConfig
    ollama: OllamaConfig = field(default_factory=lambda: OllamaConfig())
    task: TasksConfig = field(default_factory=lambda: TasksConfig())
    log: LogConfig = field(default_factory=lambda: LogConfig())


def load_config_from_json_file(json_file_path: str) -> LoomConfig:

    data: dict[str, Any]
    with open(json_file_path) as f:
        data = json.load(f)

    config: LoomConfig = from_dict(data_class=LoomConfig, data=data, config=Config(cast=[Enum]))
    return config


def write_config_to_json_file(config: LoomConfig, json_file_path: str) -> None:
    with open(json_file_path, "w") as json_file:
        json.dump(asdict(config), json_file)


def load_config_from_file(config_file_path: str) -> LoomConfig | None:

    try:
        return load_config_from_json_file(config_file_path)
    except FileNotFoundError as e:
        print(f"exception attempting to load config file {config_file_path}: {e}")
        return None


def create_new_default_config(json_config_file_path: str) -> LoomConfig:
    config = LoomConfig(model=ModelConfig(model="qwen2.5-coder:14b", think=False))
    write_config_to_json_file(config=config, json_file_path=json_config_file_path)
    print(f"new config created at {json_config_file_path}")
    return config


def configure_from_json_file(json_config_file_path: str = CONFIG_FILE_PATH) -> LoomConfig:

    if (config := load_config_from_file(json_config_file_path)) is not None:
        return config

    print("not configured")
    return create_new_default_config(json_config_file_path)
