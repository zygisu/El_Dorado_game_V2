import random
import time
import os
from turns_logic import place_pawns
from colorama import Fore, Style, Back, init

init(autoreset=True)


def generate_board(player1_color, player2_color):
    rows = 7
    cols = 7
    board = [["" for _ in range(cols)] for _ in range(rows)]

    coordinates = [[f"{chr(65 + r)}{c + 1}" for c in range(cols)] for r in range(rows)]

    start = (random.randint(0, rows - 1), random.randint(0, cols - 1))
    finish = (random.randint(0, rows - 1), random.randint(0, cols - 1))
    while finish == start:
        finish = (random.randint(0, rows - 1), random.randint(0, cols - 1))

    board[start[0]][start[1]] = f"{player1_color}{player2_color}"
    board[finish[0]][finish[1]] = colorize_value("EL")

    mm_count = random.randint(5, 7)
    for _ in range(mm_count):
        while True:
            r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
            if board[r][c] == "":
                board[r][c] = colorize_value("MM")
                break

    possible_values = ["F1", "F2", "W1", "W2", "D1", "D2"]
    weights = [2, 1, 2, 1, 2, 1]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "":
                board[r][c] = colorize_value(
                    random.choices(possible_values, weights=weights, k=1)[0]
                )

    print_board(board, coordinates)
    return board, coordinates, start, finish


def colorize_value(value):
    if value.startswith("F"):
        return Fore.GREEN + value + Style.RESET_ALL
    elif value.startswith("W"):
        return Fore.BLUE + value + Style.RESET_ALL
    elif value.startswith("D"):
        return Fore.YELLOW + value + Style.RESET_ALL
    elif value == "MM":
        return Fore.LIGHTBLACK_EX + value + Style.RESET_ALL
    elif value == "EL":
        return Fore.WHITE + Back.YELLOW + value + Style.RESET_ALL
    return value


def print_board(board, coordinates):
    col_width = 4
    col_numbers = "    " + " ".join(
        [f"{str(i + 1).center(col_width)}" for i in range(len(board[0]))]
    )
    print(col_numbers)
    print("   +" + ("-" * col_width + "+") * len(board[0]))
    for r, row in enumerate(board):
        row_str = f" {chr(65 + r)} |" + "".join(
            [f" {cell.center(col_width - 2)} |" for cell in row]
        )
        print(row_str)
        print("   +" + ("-" * col_width + "+") * len(board[0]))


def pawn_types():
    red_pawn = Fore.RED + "♙" + Style.RESET_ALL
    blue_pawn = Fore.BLUE + "♟" + Style.RESET_ALL
    return red_pawn, blue_pawn


def select_pawns():
    red_pawn, blue_pawn = pawn_types()

    print("Player 1, chose your pawn:")
    print(f" 1. Red Pawn: {red_pawn}")
    print(f" 2. Blue Pawn: {blue_pawn}")
    print()
    choice_for_pawn = input("Your pawn: ").strip()
    time.sleep(2)
    os.system("cls" if os.name == "nt" else "clear")

    if choice_for_pawn == "1":
        player1_color = red_pawn
        player2_color = blue_pawn
    elif choice_for_pawn == "2":
        player1_color = blue_pawn
        player2_color = red_pawn
    else:
        print("Invalid choice. Computer is choosing randomly...")
        time.sleep(2)
        if random.choice([True, False]):
            player1_color = red_pawn
            player2_color = blue_pawn
        else:
            player1_color = blue_pawn
            player2_color = red_pawn

    return player1_color, player2_color


original_square_values = {}


def initialize_original_square_values(board, player_positions):

    global original_square_values
    original_square_values = {}

    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if (r, c) not in player_positions.values():
                original_square_values[(r, c)] = cell


def update_board(board, player_positions, start):

    for (row, col), original_value in original_square_values.items():
        board[row][col] = original_value

    for player, position in player_positions.items():
        row, col = position

        if player == "P1":
            board[row][col] = Fore.BLUE + "♟" + Style.RESET_ALL
        elif player == "P2":
            board[row][col] = Fore.RED + "♙" + Style.RESET_ALL

    start_row, start_col = start
    if (start_row, start_col) not in player_positions.values():
        board[start_row][start_col] = original_square_values.get(
            (start_row, start_col), "  "
        )

    print_board(
        board,
        [
            [f"{chr(65 + r)}{c + 1}" for c in range(len(board[0]))]
            for r in range(len(board))
        ],
    )
    time.sleep(1)


if __name__ == "__main__":
    player1_color, player2_color = select_pawns()
    board, coordinates, start, finish = generate_board(player1_color, player2_color)
    place_pawns(board, start, player1_color, player2_color)
