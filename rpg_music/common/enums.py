from enum import Enum
from typing import Any


def deep_stringify_enums(data: Any) -> Any:
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = deep_stringify_enums(value)
    elif isinstance(data, list):
        return [deep_stringify_enums(value) for value in data]
    elif isinstance(data, Enum):
        return data.value
    return data
