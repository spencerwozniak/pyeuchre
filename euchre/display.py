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


# Card dimensions for table layout
_CARD_WIDTH = 11
_CARD_HEIGHT = 9

_EMPTY_SLOT_LINES = [
    "┌─────────┐",
    "│         │",
    "│         │",
    "│   ───   │",
    "│         │",
    "│         │",
    "│         │",
    "│         │",
    "└─────────┘",
]


def _single_card_lines(card):
    """Return 9 lines of 11 chars for one card, or placeholder if card is None."""
    if card is None:
        return list(_EMPTY_SLOT_LINES)
    return card_image(card, return_string=False)


def render_table(trick_by_seat, player_names, human_hand=None):
    """
    Render the table: Player 1 left, Player 2 top, Player 3 right, User (seat 0) bottom.
    trick_by_seat[i] = card played by seat i (or None). player_names[i] = name for seat i.
    human_hand = list of cards to show below table for the user (optional).
    """
    # Layout: 43 cols. Left card 0-10, center 16-26, right 32-42.
    # Rows: 0=label P2, 1-9=P2 card; 10=label P1/P3, 11-19=P1 left, P3 right; 20=label user, 21-29=user card.
    width = 43
    height = 30
    grid = [[" "] * width for _ in range(height)]

    def write_block(start_row, start_col, lines):
        for r, line in enumerate(lines):
            for c, ch in enumerate(line):
                if 0 <= start_row + r < height and 0 <= start_col + c < width:
                    grid[start_row + r][start_col + c] = ch

    def center_label(text, row):
        # Center text in width
        t = text[:width]
        col = (width - len(t)) // 2
        for i, ch in enumerate(t):
            if 0 <= col + i < width:
                grid[row][col + i] = ch

    # Seat 2 = top, seat 1 = left, seat 3 = right, seat 0 = bottom
    center_col = (width - _CARD_WIDTH) // 2  # 16

    # Top: Player 2 (seat 2)
    center_label(player_names[2], 0)
    write_block(1, center_col, _single_card_lines(trick_by_seat[2]))

    # Middle row: Player 1 (left), Player 3 (right) - labels on row 10
    name1, name3 = player_names[1][:11], player_names[3][:11]
    for j, ch in enumerate(name1):
        if j < width:
            grid[10][j] = ch
    for j, ch in enumerate(name3):
        col = width - len(name3) + j
        if 0 <= col < width:
            grid[10][col] = ch
    write_block(11, 0, _single_card_lines(trick_by_seat[1]))
    write_block(11, width - _CARD_WIDTH, _single_card_lines(trick_by_seat[3]))

    # Bottom: User (seat 0)
    center_label(player_names[0], 20)
    write_block(21, center_col, _single_card_lines(trick_by_seat[0]))

    lines_out = ["".join(row) for row in grid]

    if human_hand:
        lines_out.append("")
        lines_out.append("Your hand:")
        hand_str = card_image(*human_hand, return_string=True)
        lines_out.append(hand_str)

    return "\n".join(lines_out)


def print_table(trick_by_seat, player_names, human_hand=None):
    """Print the table view (see render_table)."""
    print(render_table(trick_by_seat, player_names, human_hand))


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
