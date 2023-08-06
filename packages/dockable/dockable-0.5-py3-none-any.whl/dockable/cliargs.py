from typing import Any, TypeVar

import yaml
from arketip.arketip import cast_to_type, is_type

from .load.file_loader import load_yaml
from .load.module import common_merge
from .types import Path

T = TypeVar("T")


def deep_merge(data: list[dict]) -> dict:
    data2 = common_merge(data)

    def merge_values(data: list[T]) -> T:
        if is_type(data, list[dict]):
            # https://github.com/python/mypy/issues/13800
            return deep_merge(data)  # type: ignore[return-value]
        else:
            return [x for x in data if x is not None][-1]

    return {k: merge_values(v) for k, v in data2.items()}


def process_cli_vars(values_files: list[Path] | None, overrides: list[str] | None) -> dict[str, Any]:
    _values_files = values_files if values_files else []
    _overrides = overrides if overrides else []
    from_files = [cast_to_type(load_yaml(x), dict[str, Any]) for x in _values_files]
    from_cli = [parse_command_line_var(x) for x in _overrides]
    return deep_merge(from_files + from_cli)


def parse_command_line_var(var: str) -> dict[str, Any]:
    def unfold(key: str, val: str) -> dict[str, Any]:
        match key.split(".", 1):
            case [k, v]:
                return {k: unfold(v, val)}
            case [k]:
                return {k: yaml.safe_load(val)}
            case _:
                raise ValueError("unreachable")

    return unfold(*var.split("=", 1))
