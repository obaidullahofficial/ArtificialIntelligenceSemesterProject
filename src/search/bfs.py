"""Breadth-First Search (BFS) on an unweighted graph.

The graph is represented as a dictionary mapping each node to a list of its
neighbours::

    graph = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['D', 'E'],
        'D': [],
        'E': [],
    }
"""

from collections import deque
from typing import Any, Dict, List, Optional


def bfs(
    graph: Dict[Any, List[Any]],
    start: Any,
    goal: Any,
) -> Optional[List[Any]]:
    """Return the shortest path from *start* to *goal* using BFS.

    Parameters
    ----------
    graph:
        Adjacency list representation of the graph.
    start:
        The starting node.
    goal:
        The target node.

    Returns
    -------
    list or None
        The path as a list of nodes from *start* to *goal*, or ``None`` if no
        path exists.
    """
    if start == goal:
        return [start]

    visited = {start}
    # Each queue entry is the path taken so far.
    queue: deque = deque([[start]])

    while queue:
        path = queue.popleft()
        node = path[-1]

        for neighbour in graph.get(node, []):
            if neighbour == goal:
                return path + [neighbour]
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(path + [neighbour])

    return None
