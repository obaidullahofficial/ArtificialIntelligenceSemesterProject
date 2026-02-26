"""Tests for the Tic-Tac-Toe game and Minimax AI."""

import pytest
from src.games.tictactoe import TicTacToe
from src.games.minimax import best_move, minimax


# ---------------------------------------------------------------------------
# TicTacToe board tests
# ---------------------------------------------------------------------------

class TestTicTacToe:
    def test_empty_board_has_nine_moves(self):
        game = TicTacToe()
        assert game.available_moves() == list(range(9))

    def test_make_move_reduces_available_moves(self):
        game = TicTacToe().make_move(4)
        assert 4 not in game.available_moves()
        assert len(game.available_moves()) == 8

    def test_player_alternates(self):
        game = TicTacToe()
        assert game.current_player == "X"
        game = game.make_move(0)
        assert game.current_player == "O"
        game = game.make_move(1)
        assert game.current_player == "X"

    def test_winner_row(self):
        # X wins on the top row
        board = ["X", "X", "X", "O", "O", None, None, None, None]
        game = TicTacToe(board)
        assert game.winner() == "X"

    def test_winner_column(self):
        board = ["O", "X", None, "O", "X", None, "O", None, None]
        game = TicTacToe(board)
        assert game.winner() == "O"

    def test_winner_diagonal(self):
        board = ["X", "O", "O", None, "X", "O", None, None, "X"]
        game = TicTacToe(board)
        assert game.winner() == "X"

    def test_no_winner_on_empty_board(self):
        assert TicTacToe().winner() is None

    def test_draw_detection(self):
        # Full board with no winner
        board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
        game = TicTacToe(board)
        assert game.winner() is None
        assert game.is_draw()

    def test_is_terminal_on_win(self):
        board = ["X", "X", "X", "O", "O", None, None, None, None]
        assert TicTacToe(board).is_terminal()

    def test_is_terminal_on_draw(self):
        board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
        assert TicTacToe(board).is_terminal()

    def test_is_not_terminal_on_empty_board(self):
        assert not TicTacToe().is_terminal()

    def test_occupied_cell_raises(self):
        game = TicTacToe().make_move(0)
        with pytest.raises(ValueError):
            game.make_move(0)

    def test_immutability(self):
        original = TicTacToe()
        _ = original.make_move(4)
        assert original.board[4] is None


# ---------------------------------------------------------------------------
# Minimax / best_move tests
# ---------------------------------------------------------------------------

class TestMinimax:
    def test_ai_wins_when_possible(self):
        # O can win immediately by playing index 2
        board = ["O", "O", None, "X", "X", None, None, None, None]
        game = TicTacToe(board, current_player="O")
        assert best_move(game) == 2

    def test_ai_blocks_human_win(self):
        # X would win at index 2 — AI (O) must block
        board = ["X", "X", None, "O", None, None, None, None, None]
        game = TicTacToe(board, current_player="O")
        assert best_move(game) == 2

    def test_ai_prefers_win_over_block(self):
        # O can win at 6 or should block X at 2, but winning is preferred
        board = ["O", "O", None, "X", "X", None, None, None, None]
        game = TicTacToe(board, current_player="O")
        move = best_move(game)
        assert move == 2  # Winning move

    def test_no_moves_raises(self):
        board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
        game = TicTacToe(board)
        with pytest.raises(ValueError):
            best_move(game)

    def test_minimax_draw_on_empty_board(self):
        # Perfect play from both sides always results in a draw.
        game = TicTacToe()  # X moves first
        score = minimax(game, maximising=False)  # X is minimising
        assert score == 0.0

    def test_minimax_o_wins_immediately(self):
        board = ["O", "O", None, "X", "X", None, None, None, None]
        game = TicTacToe(board, current_player="O")
        child = game.make_move(2)  # O wins
        score = minimax(child, maximising=False)
        assert score == 1.0

    def test_best_move_on_near_full_board(self):
        # Only one move left
        board = ["X", "O", "X", "X", "O", "O", "O", "X", None]
        game = TicTacToe(board, current_player="O")
        assert best_move(game) == 8
