"""Console display and prompts for Euchre."""

from .constants import SUIT_SYMBOLS

BANNER = r"""
===========================================================================================================================================================
 .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. 
 | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. |
 | |   ______     | | |  ____  ____  | | |  _________   | | | _____  _____ | | |     ______   | | |  ____  ____  | | |  _______     | | |  _________   | |
 | |  |_   __ \   | | | |_  _||_  _| | | | |_   ___  |  | | ||_   _||_   _|| | |   .' ___  |  | | | |_   ||   _| | | | |_   __ \    | | | |_   ___  |  | |
 | |    | |__) |  | | |   \ \  / /   | | |   | |_  \_|  | | |  | |    | |  | | |  / .'   \_|  | | |   | |__| |   | | |   | |__) |   | | |   | |_  \_|  | |
 | |    |  ___/   | | |    \ \/ /    | | |   |  _|  _   | | |  | '    ' |  | | |  | |         | | |   |  __  |   | | |   |  __ /    | | |   |  _|  _   | |
 | |   _| |_      | | |    _|  |_    | | |  _| |___/ |  | | |   \ `--' /   | | |  \ `.___.'\  | | |  _| |  | |_  | | |  _| |  \ \_  | | |  _| |___/ |  | |
 | |  |_____|     | | |   |______|   | | | |_________|  | | |    `.__.'    | | |   `._____.'  | | | |____||____| | | | |____| |___| | | | |_________|  | |
 | |              | | |              | | |              | | |              | | |              | | |              | | |              | | |              | |
 | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' |
  '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' 
===========================================================================================================================================================
"""


def card_image(*cards, return_string=True):
    """Render one or more cards as ASCII art. Each card has .suit and .rank."""
    lines = [[] for _ in range(9)]
    for card in cards:
        rank = card.rank if card.rank == "10" else card.rank[0]
        space = "" if card.rank == "10" else " "
        symbol = SUIT_SYMBOLS.get(card.suit, "?")
        lines[0].append("┌─────────┐")
        lines[1].append("│{}{}       │".format(rank, space))
        lines[2].append("│         │")
        lines[3].append("│         │")
        lines[4].append("│    {}    │".format(symbol))
        lines[5].append("│         │")
        lines[6].append("│         │")
        lines[7].append("│       {}{}│".format(space, rank))
        lines[8].append("└─────────┘")
    result = ["".join(line) for line in lines]
    if return_string:
        return "\n".join(result)
    return result


def print_banner():
    print(BANNER)


def print_hand(hand):
    """Print a hand of cards using card_image."""
    if not hand:
        return
    print(card_image(*hand))


def print_card_indices():
    """Print the (1) (2) ... indices under a row of cards."""
    print("    (1)    " + "    (2)    " + "    (3)    " + "    (4)    " + "    (5)    ")


def prompt_player_name():
    return input("Enter your name to begin: ").strip() or "Player"


def prompt_pickup_or_pass():
    print("Would you like to pass or pick up?")
    while True:
        option = input().strip()
        if not option:
            continue
        opt = option.capitalize()
        if opt == "Pass":
            return "pass"
        if opt in ("Pick up", "Pick it up"):
            return "pickup"
        print("That's not an option! Say 'Pass' or 'Pick up'.")


def prompt_discard(hand_size=5):
    print("Which card would you like to get rid of?")
    print("")
    parts = ["    ({})    ".format(i + 1) for i in range(hand_size)]
    print("".join(parts))
    while True:
        try:
            idx = int(input())
            if 1 <= idx <= hand_size:
                return idx - 1
        except ValueError:
            pass
        print("You must pick a card between 1 and {}!".format(hand_size))


def prompt_call_trump(upcard_suit):
    print("What would you like to call? (You cannot call the same suit as the flipped card.)")
    valid = ("Spades", "Hearts", "Clubs", "Diamonds")
    while True:
        option = input().strip().capitalize()
        if option == upcard_suit:
            print("You can't call what you just flipped over!")
            continue
        if option in valid:
            return option
        print("Please enter a suit: Spades, Hearts, Clubs, or Diamonds.")


def prompt_play_card(hand_size):
    print("Which card would you like to throw?")
    print("")
    parts = ["    ({})    ".format(i + 1) for i in range(hand_size)]
    print("".join(parts))
    while True:
        try:
            idx = int(input())
            if 1 <= idx <= hand_size:
                return idx - 1
        except ValueError:
            pass
        print("You must pick a card between 1 and {}!".format(hand_size))


def clear_screen():
    print("\n" * 100)
