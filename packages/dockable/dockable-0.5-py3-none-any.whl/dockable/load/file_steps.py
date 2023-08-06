from typing import ParamSpec

import yaml
from arketip.arketip import cast_to_type
from jinja2 import ChainableUndefined  # type: ignore

from ..types import Handler, InlineHandler, LocalContext, Path, Step
from .file_loader import load_jinja, load_multifile

P = ParamSpec("P")


def load_inline_handler(data: str) -> InlineHandler:
    parsed = yaml.safe_load(data)
    return cast_to_type(parsed, InlineHandler)


def load_template_step(data: str) -> tuple[str, Handler]:
    rendered = load_jinja(data, undefined=ChainableUndefined)()
    parsed = load_inline_handler(rendered)

    def _load(*args: P.args, **kwargs: P.kwargs) -> list[Step]:
        rendered = load_jinja(data)(*args, **kwargs)
        parsed = load_inline_handler(rendered)
        return parsed["steps"]

    return parsed["name"], _load


def load_text_step(data: str) -> tuple[str, Handler]:
    rendered = yaml.safe_load(data)
    parsed = load_inline_handler(rendered)
    return parsed["name"], lambda: parsed["steps"]


def load_file_steps(file: Path) -> LocalContext:
    data = load_multifile(file)
    load_fnc = load_template_step if file.endswith(".jinja") else load_text_step
    data2 = [load_fnc(x) for x in data]
    return {k: v for k, v in data2}
