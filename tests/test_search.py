"""Tests for BFS, DFS, and A* search algorithms."""

import pytest
from src.search.bfs import bfs
from src.search.dfs import dfs
from src.search.astar import astar


# ---------------------------------------------------------------------------
# Shared graph fixtures
# ---------------------------------------------------------------------------

SIMPLE_GRAPH = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["F"],
    "F": [],
}

WEIGHTED_GRAPH = {
    "A": [("B", 1), ("C", 4)],
    "B": [("C", 2), ("D", 5)],
    "C": [("D", 1)],
    "D": [],
}

DISCONNECTED_GRAPH = {
    "A": ["B"],
    "B": [],
    "C": ["D"],
    "D": [],
}


# ---------------------------------------------------------------------------
# BFS tests
# ---------------------------------------------------------------------------

class TestBFS:
    def test_finds_path(self):
        path = bfs(SIMPLE_GRAPH, "A", "F")
        assert path is not None
        assert path[0] == "A"
        assert path[-1] == "F"

    def test_shortest_path(self):
        # BFS should find A -> C -> F (length 3), not A -> B -> E -> F (length 4)
        path = bfs(SIMPLE_GRAPH, "A", "F")
        assert path == ["A", "C", "F"]

    def test_same_start_and_goal(self):
        assert bfs(SIMPLE_GRAPH, "A", "A") == ["A"]

    def test_no_path(self):
        assert bfs(DISCONNECTED_GRAPH, "A", "C") is None

    def test_direct_neighbour(self):
        path = bfs(SIMPLE_GRAPH, "A", "B")
        assert path == ["A", "B"]

    def test_empty_graph_no_path(self):
        assert bfs({}, "A", "B") is None


# ---------------------------------------------------------------------------
# DFS tests
# ---------------------------------------------------------------------------

class TestDFS:
    def test_finds_path(self):
        path = dfs(SIMPLE_GRAPH, "A", "F")
        assert path is not None
        assert path[0] == "A"
        assert path[-1] == "F"

    def test_same_start_and_goal(self):
        assert dfs(SIMPLE_GRAPH, "A", "A") == ["A"]

    def test_no_path(self):
        assert dfs(DISCONNECTED_GRAPH, "A", "C") is None

    def test_direct_neighbour(self):
        path = dfs(SIMPLE_GRAPH, "A", "B")
        assert path == ["A", "B"]

    def test_path_visits_each_node_once(self):
        path = dfs(SIMPLE_GRAPH, "A", "F")
        assert len(path) == len(set(path)), "DFS path should not revisit nodes"


# ---------------------------------------------------------------------------
# A* tests
# ---------------------------------------------------------------------------

def zero_heuristic(node, goal):
    """Trivial admissible heuristic (turns A* into Dijkstra's)."""
    return 0


def manhattan(node, goal):
    """2-D Manhattan distance heuristic for grid-coordinate nodes."""
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


class TestAStar:
    def test_finds_optimal_path(self):
        # Optimal: A -> B -> C -> D with cost 1+2+1 = 4 (vs A -> C -> D cost 4+1=5)
        path = astar(WEIGHTED_GRAPH, "A", "D", zero_heuristic)
        assert path == ["A", "B", "C", "D"]

    def test_same_start_and_goal(self):
        path = astar(WEIGHTED_GRAPH, "A", "A", zero_heuristic)
        assert path == ["A"]

    def test_no_path(self):
        weighted_disconnected = {
            "A": [("B", 1)],
            "B": [],
            "C": [("D", 1)],
            "D": [],
        }
        assert astar(weighted_disconnected, "A", "C", zero_heuristic) is None

    def test_grid_with_manhattan_heuristic(self):
        # 3x3 grid graph; nodes are (row, col) tuples.
        grid_graph = {
            (0, 0): [((0, 1), 1), ((1, 0), 1)],
            (0, 1): [((0, 0), 1), ((0, 2), 1), ((1, 1), 1)],
            (0, 2): [((0, 1), 1), ((1, 2), 1)],
            (1, 0): [((0, 0), 1), ((1, 1), 1), ((2, 0), 1)],
            (1, 1): [((0, 1), 1), ((1, 0), 1), ((1, 2), 1), ((2, 1), 1)],
            (1, 2): [((0, 2), 1), ((1, 1), 1), ((2, 2), 1)],
            (2, 0): [((1, 0), 1), ((2, 1), 1)],
            (2, 1): [((2, 0), 1), ((2, 2), 1), ((1, 1), 1)],
            (2, 2): [((2, 1), 1), ((1, 2), 1)],
        }
        path = astar(grid_graph, (0, 0), (2, 2), manhattan)
        assert path is not None
        assert path[0] == (0, 0)
        assert path[-1] == (2, 2)
        # Optimal path length on unit grid is Manhattan distance + 1 nodes
        assert len(path) == 5
