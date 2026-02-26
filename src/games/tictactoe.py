"""Tic-Tac-Toe board representation and game logic."""

from __future__ import annotations

from typing import List, Optional


class TicTacToe:
    """A Tic-Tac-Toe game.

    The board is a flat list of 9 cells indexed 0-8::

        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8

    Each cell contains ``'X'``, ``'O'``, or ``None``.

    Parameters
    ----------
    board:
        Optional initial board state (list of 9 elements).  Defaults to an
        empty board.
    current_player:
        ``'X'`` or ``'O'``.  Defaults to ``'X'``.
    """

    WINNING_LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6),              # diagonals
    ]

    def __init__(
        self,
        board: Optional[List[Optional[str]]] = None,
        current_player: str = "X",
    ) -> None:
        self.board: List[Optional[str]] = board[:] if board else [None] * 9
        self.current_player = current_player

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def available_moves(self) -> List[int]:
        """Return the indices of empty cells."""
        return [i for i, cell in enumerate(self.board) if cell is None]

    def winner(self) -> Optional[str]:
        """Return ``'X'`` or ``'O'`` if that player has won, else ``None``."""
        for a, b, c in self.WINNING_LINES:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def is_terminal(self) -> bool:
        """Return ``True`` if the game is over (win or draw)."""
        return self.winner() is not None or not self.available_moves()

    def is_draw(self) -> bool:
        """Return ``True`` if the game ended in a draw."""
        return self.winner() is None and not self.available_moves()

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------

    def make_move(self, index: int) -> "TicTacToe":
        """Return a new board after placing the current player's mark.

        Parameters
        ----------
        index:
            Cell index (0-8).

        Raises
        ------
        ValueError
            If the cell is already occupied.
        """
        if self.board[index] is not None:
            raise ValueError(f"Cell {index} is already occupied.")
        new_board = self.board[:]
        new_board[index] = self.current_player
        next_player = "O" if self.current_player == "X" else "X"
        return TicTacToe(new_board, next_player)

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        symbols = [cell if cell else "." for cell in self.board]
        rows = [
            " | ".join(symbols[0:3]),
            "---------",
            " | ".join(symbols[3:6]),
            "---------",
            " | ".join(symbols[6:9]),
        ]
        return "\n".join(rows)


def play_game() -> None:
    """Run a human-vs-AI game in the terminal."""
    game = TicTacToe()
    # Import here to avoid circular dependency at module load time.
    from src.games.minimax import best_move  # noqa: PLC0415

    print("Tic-Tac-Toe: You are 'X', AI is 'O'.")
    print("Enter a cell number (0-8) to make a move.\n")
    print(game)
    print()

    while not game.is_terminal():
        if game.current_player == "X":
            while True:
                try:
                    move = int(input("Your move (0-8): "))
                    game = game.make_move(move)
                    break
                except (ValueError, IndexError, KeyError):
                    print("Invalid move. Try again.")
        else:
            move = best_move(game)
            print(f"AI plays: {move}")
            game = game.make_move(move)

        print()
        print(game)
        print()

    winner = game.winner()
    if winner:
        print(f"{'You win!' if winner == 'X' else 'AI wins!'}")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    play_game()
