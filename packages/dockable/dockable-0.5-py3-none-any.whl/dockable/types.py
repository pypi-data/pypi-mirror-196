from collections.abc import Callable
from typing import TypeAlias, TypedDict

Path: TypeAlias = str
Hash: TypeAlias = str
Dependencies: TypeAlias = set[str]
Step: TypeAlias = dict | str
StepArgs: TypeAlias = dict | list | str


class InlineHandler(TypedDict):
    name: str
    steps: list[Step]


FuncHandlers: TypeAlias = dict[str, str]
Handler: TypeAlias = Callable[..., list[Step]]
LocalContext: TypeAlias = dict[str, Handler]
Context: TypeAlias = dict[str, LocalContext]
