import networkx as nx
from arketip.arketip import cast_to_type

from .graph import get_children, get_step


def render_steps(G: nx.DiGraph) -> list[str]:
    data = [get_step(G, x) for x in nx.dfs_postorder_nodes(G) if len(get_children(G, x)) == 0]
    # leaves by definition must be str and cannot be dict,
    # as otherwise recursion would not have stopped
    # the type-cast here is just to also tell this to mypy
    return [cast_to_type(x, str) for x in data]


def render(data: dict) -> str:
    data2 = render_steps(data["steps"])
    return "\n".join(data2)
