"""Card model and trump-aware ordering for Euchre."""

from .constants import (
    LEFT_BOWER_SUIT,
    RANKS,
    RANK_ORDER,
    SUITS,
)


class Card:
    """A single Euchre card. Ordering depends on trump (use ordering_value(trump))."""

    __slots__ = ("suit", "rank")

    def __init__(self, suit: str, rank: str):
        self.suit = suit.capitalize() if isinstance(suit, str) else suit
        self.rank = rank
        if self.suit not in SUITS or self.rank not in RANKS:
            raise ValueError(f"Invalid card: {suit} {rank}")

    def is_right_bower(self, trump: str) -> bool:
        return self.rank == "Jack" and self.suit == trump

    def is_left_bower(self, trump: str) -> bool:
        return self.rank == "Jack" and self.suit == LEFT_BOWER_SUIT.get(trump)

    def is_trump(self, trump: str) -> bool:
        if self.suit == trump:
            return True
        if self.rank == "Jack" and self.suit == LEFT_BOWER_SUIT.get(trump):
            return True
        return False

    def ordering_value(self, trump: str) -> int:
        """
        Return a comparable value for this card when trump is set. Higher = wins.
        Right bower > left bower > other trump (A high) > off-suit (A high).
        """
        if self.is_right_bower(trump):
            return 100
        if self.is_left_bower(trump):
            return 99
        if self.suit == trump:
            # Trump suit, non-bower: A=14, K=13, Q=12, 10=11, 9=10
            return 10 + (RANK_ORDER[self.rank] + 1)  # 9->10, Ace->15, but Jack already handled
        # Off-suit: 9=0 .. Ace=5 (so we don't overlap trump range)
        return RANK_ORDER[self.rank]

    def effective_suit(self, trump: str) -> str:
        """Suit for follow-suit rules: left bower counts as trump."""
        if self.is_left_bower(trump):
            return trump
        return self.suit

    def __repr__(self) -> str:
        return f"Card({self.suit!r}, {self.rank!r})"

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.suit == other.suit and self.rank == other.rank

    def __hash__(self) -> int:
        return hash((self.suit, self.rank))
