"""
Console-based Tic-Tac-Toe with a movable cursor controlled by W/A/S/D.

Usage:
    python TicTacToeConsole.py

Controls (type command then press Enter):
    W / A / S / D -> move cursor (Up / Left / Down / Right)
    Enter (empty line) or single Space -> place current player's mark
    Q -> quit game

This implementation does not rely on curses or external libraries.
It uses simple input() calls and ANSI escape sequences for redrawing.
"""

from typing import List, Optional, Tuple


def clear_screen() -> None:
    """Clear the console using ANSI escape codes."""
    print("\033[2J\033[H", end="")


def new_board() -> List[List[str]]:
    """Return a 3×3 board populated with blanks."""
    return [[" " for _ in range(3)] for _ in range(3)]


def render(
    board: List[List[str]],
    cursor: Tuple[int, int],
    current_player: str,
    message: str,
) -> None:
    """Draw the board, cursor, and status text."""
    clear_screen()
    print("=== Tic-Tac-Toe (W/A/S/D to move, Enter/Space to place, Q to quit) ===")
    print(f"Current player: {current_player}\n")

    cur_r, cur_c = cursor
    for r in range(3):
        row_display = []
        for c in range(3):
            cell = board[r][c]
            if cell == " ":
                cell = " "
            cell_text = f"[{cell}]" if (r, c) == (cur_r, cur_c) else f" {cell} "
            row_display.append(cell_text)
        print(" | ".join(row_display))
        if r < 2:
            print("---+-----+---")

    if message:
        print(f"\n{message}")


def check_winner(board: List[List[str]]) -> Optional[str]:
    """Return the winning mark ('X' or 'O') if present, else None."""
    lines = []
    for i in range(3):
        lines.append(board[i])  # row
        lines.append([board[0][i], board[1][i], board[2][i]])  # column

    lines.append([board[0][0], board[1][1], board[2][2]])  # diag 1
    lines.append([board[0][2], board[1][1], board[2][0]])  # diag 2

    for line in lines:
        if line[0] != " " and line.count(line[0]) == 3:
            return line[0]
    return None


def board_full(board: List[List[str]]) -> bool:
    """Return True if no cells remain empty."""
    return all(cell != " " for row in board for cell in row)


def main() -> None:
    board = new_board()
    cursor = (0, 0)
    player = "X"
    message = ""
    game_over = False

    while True:
        render(board, cursor, player, message)

        if game_over:
            choice = input("Game over. Play again? (y/n): ").strip().lower()
            if choice == "y":
                board = new_board()
                cursor = (0, 0)
                player = "X"
                message = ""
                game_over = False
                continue
            print("Thanks for playing!")
            break

        command = input("Command: ").strip().lower()

        # Quit request
        if command == "q":
            print("Quitting. Goodbye!")
            break

        # Empty command (just Enter) or single space => place mark
        if command == "" or command == " ":
            r, c = cursor
            if board[r][c] != " ":
                message = "Cell already filled. Choose another spot."
                continue

            board[r][c] = player
            winner = check_winner(board)
            if winner:
                message = f"Player {winner} wins!"
                game_over = True
                continue

            if board_full(board):
                message = "It's a draw!"
                game_over = True
                continue

            player = "O" if player == "X" else "X"
            message = ""
            continue

        if not command:
            message = "Use W/A/S/D to move or Enter/Space to place."
            continue

        r, c = cursor
        key = command[0]
        if key == "w" and r > 0:
            cursor = (r - 1, c)
            message = ""
        elif key == "s" and r < 2:
            cursor = (r + 1, c)
            message = ""
        elif key == "a" and c > 0:
            cursor = (r, c - 1)
            message = ""
        elif key == "d" and c < 2:
            cursor = (r, c + 1)
            message = ""
        else:
            message = "Invalid move. Cursor cannot leave board."


if __name__ == "__main__":
    main()


