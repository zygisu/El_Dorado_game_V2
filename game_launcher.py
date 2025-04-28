# Black after ###########################
import pyfiglet
import time
import json
import os


def welcome_message():
    GOLD = "\033[1;33m"
    RESET = "\033[0m"

    text = "El Dorado"
    title = pyfiglet.figlet_format(text)

    print(f"{GOLD}{title}{RESET}")
    print("Screen, not a board, game :)")
    time.sleep(3)
    os.system("cls" if os.name == "nt" else "clear")


def mode_select_launch():
    while True:
        print("1. New Game")
        print("2. Continue Game")
        print("3. Statistics")
        print("4. Game Rules")
        print("5. Exit Game")
        choice = input(f"\nSelect a game mode: ").strip()

        if choice == "1":
            os.system("cls" if os.name == "nt" else "clear")
            from main import start_new_game

            start_new_game()
        elif choice == "2":
            if os.path.exists("game_save.json"):
                os.system("cls" if os.name == "nt" else "clear")
                from main import continue_game

                continue_game()
            else:
                print("No saved game found. Please start a new game.")
                time.sleep(2)
        elif choice == "3":
            os.system("cls" if os.name == "nt" else "clear")
            with open("statistics.json", "r") as stats_file:
                stats = json.load(stats_file)
                print(f"Games launched: {stats['launched']}")
                print(f"Games finished: {stats['finished']}")
                print(f"Total moves made: {stats['moves']}")
            input("\nPress Enter to return to the mode list...")
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")
        elif choice == "4":
            os.system("cls" if os.name == "nt" else "clear")
            try:
                with open("rules.json", "r") as rules_file:
                    rules = json.load(rules_file)
                    print("Game Rules:\n")
                    for rule_set in rules:  # Iterate over the list
                        for key, value in rule_set.items():  # Iterate over each dictionary
                            print(f"{key} {value}")
            except Exception as e:
                print(f"Error reading rules file: {e}")
            input("\nPress Enter to return to the mode list...")
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")
        elif choice == "5":
            print("Thank you for playing El Dorado!")
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")
            exit()
        else:
            print("Invalid choice. Please try again.")
            time.sleep(2)
            os.system("cls" if os.name == "nt" else "clear")
