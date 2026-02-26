"""Depth-First Search (DFS) on an unweighted graph."""

from typing import Any, Dict, List, Optional


def dfs(
    graph: Dict[Any, List[Any]],
    start: Any,
    goal: Any,
    _visited: Optional[set] = None,
    _path: Optional[List[Any]] = None,
) -> Optional[List[Any]]:
    """Return a path from *start* to *goal* using DFS (recursive).

    Parameters
    ----------
    graph:
        Adjacency list representation of the graph.
    start:
        The current node being explored.
    goal:
        The target node.

    Returns
    -------
    list or None
        A path as a list of nodes from *start* to *goal*, or ``None`` if no
        path exists.
    """
    if _visited is None:
        _visited = set()
    if _path is None:
        _path = []

    _visited.add(start)
    _path = _path + [start]

    if start == goal:
        return _path

    for neighbour in graph.get(start, []):
        if neighbour not in _visited:
            result = dfs(graph, neighbour, goal, _visited, _path)
            if result is not None:
                return result

    return None
