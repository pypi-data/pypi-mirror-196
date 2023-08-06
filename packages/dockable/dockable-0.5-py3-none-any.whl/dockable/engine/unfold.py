import networkx as nx

from dockable.types import Context, Step, StepArgs

from .graph import LinkFnc, add_step, dangling_nodes, get_step, has_step, link_child, link_need

default = "dockable.raw"


def resolve_dep(key: str, curr: str = default, default: str = default) -> tuple[str, str]:
    if key.startswith("."):  # relative
        return curr, key[1:]
    elif "." in key:  # absolute
        mod, fnc = key.rsplit(".", 1)
        return mod, fnc
    else:  # default
        return default, key


def extract_special_keys(step: dict) -> tuple[dict, list[Step] | None]:
    match step:
        case {"needs": needs, **rest}:
            return rest, needs
        case _:
            return step, None


def unpack_step(step: dict) -> tuple[str, StepArgs]:
    if len(step.keys()) != 1:
        raise ValueError("only one handler per step allowed")
    else:
        return [(k, v) for k, v in step.items()][0]


def invoke_step(ctx: Context, curr: str, fnc: str, v: StepArgs) -> list[Step]:
    if curr not in ctx:
        raise ValueError(f"dockable module {curr} not found")
    if fnc not in ctx[curr]:
        raise ValueError(f"dockable module {curr} did not define {fnc}")
    match v:
        case dict() as d:
            return ctx[curr][fnc](**d)
        case list() as items:
            return ctx[curr][fnc](*items)
        case str() as s:
            return ctx[curr][fnc](s)
        case None:
            return ctx[curr][fnc]()
        case _:
            raise ValueError("unreachable")


def unfold_step(G: nx.DiGraph, ctx: Context, step: dict, curr: str = default, default: str = default) -> None:
    s, n = extract_special_keys(step)
    k, v = unpack_step(s)
    c, fnc = resolve_dep(k, curr=curr, default=default)
    steps = invoke_step(ctx, c, fnc, v)
    needs = n if n is not None else [get_step(G, x) for x in dangling_nodes(G)]
    unfold_steps(G, ctx, needs, c, parent=step, link=link_need)
    unfold_steps(G, ctx, steps, c, parent=step)


def unfold_steps(
    G: nx.DiGraph,
    ctx: Context,
    steps: list[Step],
    curr: str = default,
    default: str = default,
    parent: Step | None = None,
    link: LinkFnc = link_child,
) -> None:
    for x in steps:
        to_add = not has_step(G, x)
        if to_add:
            add_step(G, x)
        if parent is not None:
            link(G, parent, x)
        if to_add and type(x) is dict:
            unfold_step(G, ctx, x, curr=curr, default=default)


def unfold(ctx: Context, data: dict) -> dict:
    meta_steps: list[Step] = [{k: v} for k, v in data.items() if k not in ["dependencies", "steps", "name"]]
    G = nx.DiGraph()
    unfold_steps(G, ctx, meta_steps, default="dockable.meta")
    unfold_steps(G, ctx, data.get("steps", []))
    return {**data, "steps": G}
