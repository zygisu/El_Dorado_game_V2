import json
from game_launcher import mode_select_launch, welcome_message
import time
import os
from board import (
    generate_board,
    select_pawns,
    update_board,
    print_board,
    initialize_original_square_values,
    original_square_values,
)
from turns_logic import place_pawns, move_player
from cards import Deck


def save_game_progress(
    board, player_positions, start, finish, coordinates, deck1, deck2, current_player
):
    try:
        print("Saving game progress...")
        time.sleep(2)

        if (
            not board
            or not player_positions
            or not start
            or not finish
            or not coordinates
            or not deck1
            or not deck2
            or not current_player
        ):
            print("Error: Incomplete game state. Unable to save progress.")
            return

        game_state = {
            "board": board,
            "player_positions": player_positions,
            "start": start,
            "finish": finish,
            "coordinates": coordinates,
            "deck1_hand": deck1.hand,
            "deck2_hand": deck2.hand,
            "current_player": current_player,
            "original_square_values": original_square_values,
        }
        with open("game_save.json", "w") as file:
            json.dump(game_state, file)
        print("Game progress saved successfully.")
        time.sleep(2)
        os.system("cls" if os.name == "nt" else "clear")
    except Exception as e:
        print(f"Error saving game progress: {e}")


def load_game_progress():
    try:
        print("Loading game progress...")
        if not os.path.exists("game_save.json"):
            print("No saved game file found.")
            return None

        with open("game_save.json", "r") as file:
            game_state = json.load(file)

        required_keys = [
            "board",
            "player_positions",
            "start",
            "finish",
            "coordinates",
            "deck1_hand",
            "deck2_hand",
            "current_player",
            "original_square_values",
        ]
        for key in required_keys:
            if key not in game_state:
                print(f"Error: Missing key '{key}' in saved game data.")
                return None

        global original_square_values
        original_square_values = game_state["original_square_values"]

        print("Game progress loaded successfully.")
        return game_state
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error loading saved game: {e}")
        return None


def start_new_game():
    player1_color, player2_color = select_pawns()
    board, coordinates, start, finish = generate_board(player1_color, player2_color)
    place_pawns(board, start, player1_color, player2_color)

    player_positions = {"P1": start, "P2": start}
    deck1 = Deck("cards.json")
    deck2 = Deck("cards.json")
    deck1.draw_hand()
    deck2.draw_hand()

    initialize_original_square_values(board, player_positions)

    current_player = "P1"
    while True:
        print(f"{current_player}'s turn")
        hand = deck1.hand if current_player == "P1" else deck2.hand

        print("\nYour hand:\n")
        for card in hand:
            print(f"{card['type']}, {card['points']}, {card['field']}")

        while True:
            direction = (
                input(
                    "\nEnter direction (up, down, left, right), 'end' to end turn, or 'exit' to save and quit: "
                )
                .strip()
                .lower()
            )
            if direction in ["up", "down", "left", "right", "end", "exit"]:
                break
            print(
                "Invalid input. Please enter 'up', 'down', 'left', 'right', 'end', or 'exit'."
            )

        if direction == "exit":
            save_game_progress(
                board,
                player_positions,
                start,
                finish,
                coordinates,
                deck1,
                deck2,
                current_player,
            )
            print("Exiting to mode list...")
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")

            mode_select_launch()
            return

        if direction == "end":
            if current_player == "P1":
                deck1.draw_hand()
            else:
                deck2.draw_hand()

            current_player = "P2" if current_player == "P1" else "P1"

            print_board(board, coordinates)
            continue

        result = move_player(current_player, board, hand, player_positions, direction)
        if result == "WIN":
            GOLD = "\033[1;33m"
            RESET = "\033[0m"
            print(f"{GOLD}{current_player} reached EL DORADO! YOU WON!{RESET}")
            time.sleep(2)
            print_board(board, coordinates)
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")
            mode_select_launch()
            return
        elif result:
            update_board(board, player_positions, start)


def continue_game():
    try:
        print("Attempting to continue game...")
        game_state = load_game_progress()
        if not game_state:
            print("No saved game found. Returning to mode list...")
            time.sleep(2)
            print("Calling mode_select_launch()...")
            mode_select_launch()
            return

        print("Game state loaded successfully.")
        board = game_state["board"]
        player_positions = game_state["player_positions"]
        finish = tuple(game_state["finish"])
        start = tuple(game_state["start"])
        coordinates = game_state["coordinates"]
        deck1 = Deck("cards.json")
        deck2 = Deck("cards.json")
        deck1.hand = game_state["deck1_hand"]
        deck2.hand = game_state["deck2_hand"]
        current_player = game_state["current_player"]

        update_board(board, player_positions, start)

        while True:
            print(f"{current_player}'s turn")
            hand = deck1.hand if current_player == "P1" else deck2.hand

            print("\nYour hand:\n")
            for card in hand:
                print(f"{card['type']}, {card['points']}, {card['field']}")

            while True:
                direction = (
                    input(
                        "\nEnter direction (up, down, left, right), 'end' to end turn, or 'exit' to save and quit: "
                    )
                    .strip()
                    .lower()
                )
                if direction in ["up", "down", "left", "right", "end", "exit"]:
                    break
                print(
                    "Invalid input. Please enter 'up', 'down', 'left', 'right', 'end', or 'exit'."
                )

            if direction == "exit":
                save_game_progress(
                    board,
                    player_positions,
                    start,
                    finish,
                    coordinates,
                    deck1,
                    deck2,
                    current_player,
                )
                print("Exiting to mode list...")
                time.sleep(1)
                os.system("cls" if os.name == "nt" else "clear")
                mode_select_launch()
                return

            if direction == "end":
                if current_player == "P1":
                    deck1.draw_hand()
                else:
                    deck2.draw_hand()

                current_player = "P2" if current_player == "P1" else "P1"

                print_board(board, coordinates)
                continue

            result = move_player(
                current_player, board, hand, player_positions, direction
            )
            if result == "WIN":
                GOLD = "\033[1;33m"
                RESET = "\033[0m"
                print(f"{GOLD}{current_player} reached EL DORADO! YOU WON!{RESET}")
                time.sleep(2)
                print_board(board, coordinates)
                time.sleep(2)
                os.system("cls" if os.name == "nt" else "clear")
                mode_select_launch()
                return
            elif result:
                update_board(board, player_positions, start)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Returning to mode list...")
        time.sleep(2)
        mode_select_launch()


if __name__ == "__main__":
    welcome_message()
    mode_select_launch()
