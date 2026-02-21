# Artificial Intelligence Semester Project

A Python implementation of core Artificial Intelligence algorithms, covering classical search strategies and adversarial game-playing AI.

## Topics Covered

| Module | Algorithms |
|---|---|
| Search | Breadth-First Search (BFS), Depth-First Search (DFS), A\* Search |
| Games | Tic-Tac-Toe with Minimax & Alpha-Beta Pruning |

## Project Structure

```
src/
  search/
    __init__.py
    bfs.py          # Breadth-First Search
    dfs.py          # Depth-First Search
    astar.py        # A* Search
  games/
    __init__.py
    tictactoe.py    # Tic-Tac-Toe board + logic
    minimax.py      # Minimax with Alpha-Beta Pruning
tests/
  test_search.py
  test_tictactoe.py
```

## Requirements

- Python 3.8+

Install dependencies (none required beyond the standard library):

```bash
pip install -r requirements.txt
```

## Running the Game

Play Tic-Tac-Toe against the AI:

```bash
python -m src.games.tictactoe
```

## Running Tests

```bash
python -m pytest tests/
```

## Algorithms

### Search Algorithms

All three search algorithms operate on a generic graph represented as an adjacency list (`dict[node, list[node]]`).

- **BFS** – explores neighbours level by level; guaranteed to find the shortest path.
- **DFS** – explores as deep as possible along each branch; uses less memory than BFS.
- **A\*** – uses a heuristic to guide the search; optimal when the heuristic is admissible.

### Game-Playing AI (Tic-Tac-Toe)

The AI uses **Minimax** with **Alpha-Beta Pruning** to play optimally.  Alpha-Beta Pruning eliminates branches that cannot influence the final decision, making the search significantly faster.

## License

MIT
