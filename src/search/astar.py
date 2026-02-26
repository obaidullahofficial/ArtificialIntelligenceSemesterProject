"""A* Search on a weighted graph.

The graph is represented as a dictionary mapping each node to a list of
``(neighbour, cost)`` tuples::

    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('C', 2), ('D', 5)],
        'C': [('D', 1)],
        'D': [],
    }

A heuristic function ``h(node, goal)`` must be supplied.  For the algorithm to
be guaranteed to find the optimal path, the heuristic must be *admissible*
(i.e. it never over-estimates the true cost).
"""

import heapq
from typing import Any, Callable, Dict, List, Optional, Tuple


def astar(
    graph: Dict[Any, List[Tuple[Any, float]]],
    start: Any,
    goal: Any,
    heuristic: Callable[[Any, Any], float],
) -> Optional[List[Any]]:
    """Return the optimal path from *start* to *goal* using A*.

    Parameters
    ----------
    graph:
        Weighted adjacency list: ``{node: [(neighbour, cost), ...]}``.
    start:
        The starting node.
    goal:
        The target node.
    heuristic:
        ``h(node, goal) -> estimated_cost``.  Must be admissible.

    Returns
    -------
    list or None
        The optimal path as a list of nodes, or ``None`` if no path exists.
    """
    # Priority queue entries: (f_score, g_score, node, path)
    open_set: List[Tuple[float, float, Any, List[Any]]] = []
    heapq.heappush(open_set, (heuristic(start, goal), 0.0, start, [start]))

    # Best known g-score for each visited node.
    g_scores: Dict[Any, float] = {start: 0.0}

    while open_set:
        f, g, node, path = heapq.heappop(open_set)

        if node == goal:
            return path

        for neighbour, cost in graph.get(node, []):
            new_g = g + cost
            if new_g < g_scores.get(neighbour, float("inf")):
                g_scores[neighbour] = new_g
                new_f = new_g + heuristic(neighbour, goal)
                heapq.heappush(open_set, (new_f, new_g, neighbour, path + [neighbour]))

    return None
