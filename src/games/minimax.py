"""Minimax algorithm with Alpha-Beta Pruning for Tic-Tac-Toe.

The *maximising* player is ``'O'`` (the AI) and the *minimising* player is
``'X'`` (the human).  Scores are:

* ``+1``  – AI (``'O'``) wins
* ``-1``  – Human (``'X'``) wins
* ``0``   – draw
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.games.tictactoe import TicTacToe


def minimax(
    state: "TicTacToe",
    alpha: float = float("-inf"),
    beta: float = float("inf"),
    maximising: bool = True,
) -> float:
    """Evaluate *state* using Minimax with Alpha-Beta Pruning.

    Parameters
    ----------
    state:
        Current game state.
    alpha:
        Best score the maximising player can guarantee so far.
    beta:
        Best score the minimising player can guarantee so far.
    maximising:
        ``True`` when it is the maximising player's turn (``'O'``).

    Returns
    -------
    float
        The heuristic value of *state*.
    """
    winner = state.winner()
    if winner == "O":
        return 1.0
    if winner == "X":
        return -1.0
    if state.is_draw():
        return 0.0

    if maximising:
        value = float("-inf")
        for move in state.available_moves():
            child = state.make_move(move)
            value = max(value, minimax(child, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta cut-off
        return value
    else:
        value = float("inf")
        for move in state.available_moves():
            child = state.make_move(move)
            value = min(value, minimax(child, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break  # Alpha cut-off
        return value


def best_move(state: "TicTacToe") -> int:
    """Return the best move index for the current player using Minimax.

    The function assumes the AI always plays as ``'O'`` (maximising) and the
    human always plays as ``'X'`` (minimising).

    Parameters
    ----------
    state:
        Current game state.  It is the AI's turn.

    Returns
    -------
    int
        The cell index of the best move.

    Raises
    ------
    ValueError
        If there are no available moves.
    """
    moves = state.available_moves()
    if not moves:
        raise ValueError("No available moves.")

    is_maximising = state.current_player == "O"
    best_score = float("-inf") if is_maximising else float("inf")
    chosen_move = moves[0]

    for move in moves:
        child = state.make_move(move)
        score = minimax(child, maximising=not is_maximising)
        if is_maximising:
            if score > best_score:
                best_score = score
                chosen_move = move
        else:
            if score < best_score:
                best_score = score
                chosen_move = move

    return chosen_move
