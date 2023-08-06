from collections.abc import Callable
from typing import Any, ParamSpec

import yaml
from jinja2 import Template
from jinja2.exceptions import UndefinedError

from ..types import Path

P = ParamSpec("P")


def load_jinja(data: str, **opts: Any) -> Callable[..., str]:
    def inner(*args: P.args, **kwargs: P.kwargs) -> str:
        try:
            return Template(data, **opts).render({**kwargs, "args": [*args], "kwargs": kwargs})
        except UndefinedError as e:
            raise ValueError(f"while rendering:\n{data}") from e

    return inner


def load_yaml_or_dockerfile(data: str, kwargs: dict | None = None) -> Any:
    _kwargs = kwargs if kwargs else {}
    rendered = load_jinja(data, keep_trailing_newline=True)(**_kwargs)
    try:
        parsed = yaml.safe_load(rendered)
    except yaml.parser.ParserError:
        return rendered
    match parsed:
        case str():
            return rendered
        case _:
            return parsed


def load_yaml(file: Path) -> Any:
    with open(file) as fh:
        return yaml.safe_load(fh)


def load_multifile(file: Path) -> list[Any]:
    with open(file) as fh:
        text = fh.read()
    data = text.split("\n---\n")
    data = [*data[:-1], data[-1][:-4] if data[-1].endswith("\n---") else data[-1]]
    return [x for x in data if x.strip()]


def load_file(file: Path, kwargs: dict | None = None) -> list[Any]:
    data = load_multifile(file)
    return [load_yaml_or_dockerfile(x, kwargs) for x in data]
