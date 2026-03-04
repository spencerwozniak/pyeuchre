"""Euchre game constants."""

SUITS = ("Spades", "Diamonds", "Hearts", "Clubs")
RANKS = ("9", "10", "Jack", "Queen", "King", "Ace")

# Display: suit -> symbol
SUIT_SYMBOLS = {
    "Spades": "\u2660",
    "Diamonds": "\u2666",
    "Hearts": "\u2665",
    "Clubs": "\u2663",
}

NUM_PLAYERS = 4
CARDS_PER_HAND = 5
KITTY_SIZE = 4

# Left bower: for each trump suit, the other suit of same color (Jack of that suit = left bower)
LEFT_BOWER_SUIT = {
    "Spades": "Clubs",
    "Clubs": "Spades",
    "Hearts": "Diamonds",
    "Diamonds": "Hearts",
}

# Non-trump rank order (low to high): 9=0 .. Ace=5
RANK_ORDER = {rank: i for i, rank in enumerate(RANKS)}

# Trump rank order (excluding bowers): 9=0 .. Ace=5; bowers handled in Card.ordering_value
TRUMP_RANK_ORDER = RANK_ORDER
