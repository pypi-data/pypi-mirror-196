import os
from importlib import import_module
from typing import TypeVar

import yaml
from arketip.arketip import is_type

from ..engine.unfold import default, extract_special_keys, resolve_dep, unpack_step
from ..types import Context, Dependencies, FuncHandlers, Handler, InlineHandler, LocalContext, Path, Step
from .file_steps import load_file_steps

K = TypeVar("K")
V = TypeVar("V")


def distinct_merge(data: list[dict[K, V]]) -> dict[K, V]:
    return {k: v for x in data for k, v in x.items()}


def common_merge(data: list[dict[K, V]]) -> dict[K, list[V | None]]:
    return {k: [x.get(k) for x in data] for k in set().union(*data)}


def to_abspath(dir_path: Path, path: Path) -> Path:
    return path if os.path.isabs(path) else os.path.abspath(f"{dir_path}/{path}")


def load_module(dep: str) -> tuple[Dependencies, LocalContext]:
    def load_modules_yaml(path: Path) -> dict:
        if os.path.isfile(path):
            with open(path) as fh:
                return yaml.safe_load(fh)
        else:
            return {}

    def load_fnc_step(step: str) -> Handler:
        mod, fnc = step.split(":")
        mod_ = import_module(f".{mod}", dep)
        return getattr(mod_, fnc)

    def load_inline_text_step(step: InlineHandler) -> LocalContext:
        return {step["name"]: (lambda: step["steps"])}

    mod = import_module(dep)
    dir_path = mod.__path__[0]

    def _load(step: dict | str) -> LocalContext:
        if is_type(step, InlineHandler):
            return load_inline_text_step(step)
        elif is_type(step, FuncHandlers):
            return {k: load_fnc_step(v) for k, v in step.items()}
        elif is_type(step, Path):
            return load_file_steps(to_abspath(dir_path, step))
        else:
            raise ValueError("unreachable")

    data = load_modules_yaml(f"{dir_path}/module.yml")
    includes = [load_module(f"{dep}.{x}") for x in data.get("includes", [])]
    includes2 = [x for _, x in includes]
    dependencies = set(data.get("dependencies", [])) | {y for x, _ in includes for y in x}
    return dependencies, distinct_merge([_load(x) for x in data.get("handlers", [])] + includes2)


def guess_dependencies(data: list[Step], default: str = default) -> Dependencies:
    def _guess_dependency(step: dict) -> str | None:
        step, _ = extract_special_keys(step)
        name, _ = unpack_step(step)
        dep, _ = resolve_dep(name, curr="", default=default)
        return None if dep == "" else dep

    res = [_guess_dependency(x) for x in data if type(x) is dict]
    return {x for x in res if x}


def load_modules(data: dict) -> Context:
    meta_steps: list[Step] = [{k: v} for k, v in data.items() if k not in ["dependencies", "steps", "name"]]
    ctx: Context = {}
    queue = (
        set(data["dependencies"])
        if "dependencies" in data
        else set(data.get("extra_dependencies", []))
        | guess_dependencies(data["steps"])
        | guess_dependencies(meta_steps, default="dockable.meta")
    )
    while len(queue) > 0:
        x = queue.pop()
        if x not in data.keys():
            deps, ctx[x] = load_module(x)
            queue = queue | deps
    return ctx
