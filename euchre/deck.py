"""Deck for Euchre: 24 cards, shuffle, deal."""

import random

from .card import Card
from .constants import CARDS_PER_HAND, KITTY_SIZE, NUM_PLAYERS, RANKS, SUITS


class Deck:
    """Standard Euchre deck: 24 cards (9 through Ace in four suits)."""

    def __init__(self):
        self._cards = [
            Card(suit, rank)
            for suit in SUITS
            for rank in RANKS
        ]
        assert len(self._cards) == 24

    def shuffle(self) -> None:
        random.shuffle(self._cards)

    def deal(self):
        """
        Deal to NUM_PLAYERS hands and a kitty. Assumes deck was just shuffled.
        Returns (hands, kitty) where hands is a list of 4 lists of CARDS_PER_HAND cards,
        and kitty is a list of KITTY_SIZE cards.
        """
        n = NUM_PLAYERS * CARDS_PER_HAND
        hands = []
        for i in range(NUM_PLAYERS):
            start = i * CARDS_PER_HAND
            hands.append(self._cards[start : start + CARDS_PER_HAND])
        kitty = self._cards[n : n + KITTY_SIZE]
        return hands, kitty
