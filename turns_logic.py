import re

original_square_values = {}

RED_PAWN = "\u265f"
BLUE_PAWN = "\u2659"

FIELD_MAPPING = {"D": "Desert", "F": "Forest", "W": "Water"}

VALID_SQUARES = ["F1", "F2", "W1", "W2", "D1", "D2", "EL"]


def place_pawns(board, start, player1_color, player2_color):
    r, c = start
    original_square_values[(r, c)] = board[r][c]
    board[r][c] = f"{RED_PAWN} {BLUE_PAWN}"
    print()


def move_player(current_player, board, hand, player_positions, direction):

    global original_square_values

    current_position = player_positions[current_player]
    target_position = calculate_target_square(current_position, direction)

    if (
        target_position[0] < 0
        or target_position[0] >= len(board)
        or target_position[1] < 0
        or target_position[1] >= len(board[0])
    ):
        print("Invalid move. Target position is out of bounds.")
        return False

    target_square = board[target_position[0]][target_position[1]].strip()

    target_square = re.sub(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", "", target_square)
    target_square = re.sub(r"[^\w]", "", target_square)

    if target_square == "EL":
        return "WIN"

    valid_move, field_used = validate_move(hand, target_square)
    if not valid_move:
        print("Invalid move. Check your cards.")
        return False

    try:
        points_required = int(target_square[1])
    except (IndexError, ValueError):
        print(
            f"Error: Unable to convert target_square points to int: {target_square[1:]}"
        )
        return False

    cards_to_remove = []
    for card in hand:
        if card["field"] == field_used:
            cards_to_remove.append(card)
            points_required -= card["points"]
            if points_required <= 0:
                break

    if points_required > 0:
        print("Error: Not enough cards to make the move.")
        return False

    for card in cards_to_remove:
        hand.remove(card)

    if target_position not in original_square_values:
        original_square_values[target_position] = board[target_position[0]][
            target_position[1]
        ]

    player_positions[current_player] = target_position
    return True


def validate_move(hand, target_square):

    if target_square.strip() == "EL":
        return True, None

    clean_target_square = re.sub(
        r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", "", target_square
    )
    clean_target_square = re.sub(r"[^\w]", "", clean_target_square)

    if clean_target_square not in VALID_SQUARES:
        print(f"Error: {clean_target_square} is not a valid target square.")
        return False, None

    field_letter = clean_target_square[0]
    try:
        points = int(clean_target_square[1])
    except ValueError:
        print(
            f"Error: Unable to convert target_square points to int: {clean_target_square[1:]}"
        )
        return False, None

    field_name = FIELD_MAPPING.get(field_letter.upper())
    if not field_name:
        print(f"Error: Unknown field letter '{field_letter}' in target_square.")
        return False, None

    hand_values = calculate_hand_values(hand)

    if hand_values.get(field_name, 0) >= points:
        return True, field_name
    else:
        print("Invalid move. Check your cards.")
        return False, None


def check_winner(board, finish, player_position, player):
    if player_position == finish:
        print(f"Player {player} wins!")
        return True
    return False


def calculate_target_square(current_position, direction):
    row, col = current_position
    if direction == "up":
        return row - 1, col
    elif direction == "down":
        return row + 1, col
    elif direction == "left":
        return row, col - 1
    elif direction == "right":
        return row, col + 1
    else:
        return current_position


def calculate_hand_values(hand):
    hand_values = {"Desert": 0, "Forest": 0, "Water": 0}
    for card in hand:
        if card["field"] in hand_values:
            hand_values[card["field"]] += card["points"]
    return hand_values
