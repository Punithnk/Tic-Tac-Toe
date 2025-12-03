"""
Console Tic-Tac-Toe with a movable cursor on a 3×3 board.

Controls (using only input()):
    - W / A / S / D : move cursor (up / left / down / right)
    - Enter         : place current player's mark in selected cell
    - Space         : place current player's mark in selected cell
    - Q             : quit game

Notes:
    - Because we are not allowed to use curses or low-level key reading,
      we read whole lines with input(). Pressing just Enter produces an
      empty string, which we treat as a "place" action.
"""

from typing import List, Optional, Tuple


def clear_screen() -> None:
    """
    Clear the console using ANSI escape codes.
    This works in most modern terminals (including many Windows terminals).
    """
    print("\033[2J\033[H", end="")


def create_board() -> List[List[str]]:
    """Create an empty 3x3 Tic-Tac-Toe board."""
    return [[" " for _ in range(3)] for _ in range(3)]


def print_board(board: List[List[str]], cursor: Tuple[int, int], message: str, current_player: str) -> None:
    """
    Print the board with the cursor highlighting the selected cell.

    The cursor cell is shown in square brackets, e.g. [X] or [ ].
    Other cells are shown as plain values with padding, e.g.  X  or  O  or "   ".
    """
    clear_screen()
    row_cursor, col_cursor = cursor

    print("Tic-Tac-Toe (W/A/S/D to move, Enter/Space to place, Q to quit)")
    print(f"Current player: {current_player}")
    print()

    for r in range(3):
        row_cells = []
        for c in range(3):
            value = board[r][c]
            display_char = value if value != " " else " "
            if r == row_cursor and c == col_cursor:
                # Highlight the cursor position
                cell_str = f"[{display_char}]"
            else:
                cell_str = f" {display_char} "
            row_cells.append(cell_str)

        # Join cells with vertical separators to resemble a board
        print(" | ".join(row_cells))
        if r < 2:
            print("---+-----+---")

    print()
    if message:
        print(message)
    print()


def check_winner(board: List[List[str]]) -> Optional[str]:
    """Return 'X' or 'O' if that player has won, or None otherwise."""
    lines = []

    # Rows and columns
    for i in range(3):
        lines.append(board[i])  # row i
        lines.append([board[0][i], board[1][i], board[2][i]])  # column i

    # Diagonals
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    for line in lines:
        if line[0] != " " and line[0] == line[1] == line[2]:
            return line[0]

    return None


def is_draw(board: List[List[str]]) -> bool:
    """Return True if the board is full and there is no winner."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def main() -> None:
    board = create_board()
    cursor = (0, 0)  # (row, col)
    current_player = "X"
    message = ""
    game_over = False

    while True:
        print_board(board, cursor, message, current_player)

        if game_over:
            # Ask if user wants to play again
            choice = input("Game over. Play again? (y/n): ").strip().lower()
            if choice == "y":
                board = create_board()
                cursor = (0, 0)
                current_player = "X"
                message = ""
                game_over = False
                continue
            else:
                print("Thanks for playing!")
                break

        user_input = input(
            "Move (W/A/S/D), Enter/Space to place, Q to quit: "
        )

        # Normalize input: we only care about first non-space character
        trimmed = user_input.strip().lower()

        if trimmed == "q":
            print("Quitting game. Goodbye!")
            break

        # Place mark if the user pressed just Enter (empty string)
        # or a single space.
        if user_input == "" or user_input == " ":
            row, col = cursor
            if board[row][col] != " ":
                message = "Invalid move: cell already filled. Choose another cell."
                continue

            board[row][col] = current_player

            # Check for winner or draw
            winner = check_winner(board)
            if winner:
                message = f"Player {winner} wins!"
                game_over = True
                continue

            if is_draw(board):
                message = "It's a draw!"
                game_over = True
                continue

            # Switch player
            current_player = "O" if current_player == "X" else "X"
            message = ""
            continue

        # If not placing, interpret as movement (W/A/S/D)
        if not trimmed:
            # User entered only spaces; ignore
            message = "Please enter W/A/S/D to move or Enter/Space to place."
            continue

        key = trimmed[0]
        row, col = cursor

        if key == "w" and row > 0:
            row -= 1
            message = ""
        elif key == "s" and row < 2:
            row += 1
            message = ""
        elif key == "a" and col > 0:
            col -= 1
            message = ""
        elif key == "d" and col < 2:
            col += 1
            message = ""
        else:
            message = "Invalid move: cannot move outside the board."

        cursor = (row, col)


if __name__ == "__main__":
    main()


