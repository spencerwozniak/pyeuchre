"""Player base, HumanPlayer, and BotPlayer with single strategy."""

from .constants import SUITS
from .card import Card


def count_suits(hand):
    """Return dict mapping suit -> count of cards in that suit (by physical suit)."""
    counts = {s: 0 for s in SUITS}
    for card in hand:
        counts[card.suit] = counts.get(card.suit, 0) + 1
    return counts


def want_pickup(hand, upcard, threshold=3):
    """True if bot wants to order up the upcard (has >= threshold in that suit)."""
    counts = count_suits(hand)
    return counts.get(upcard.suit, 0) >= threshold


def call_trump(hand, upcard, must_call=False):
    """
    Choose a trump suit when passing on the upcard. Picks a suit with >= 3 cards.
    upcard.suit is forbidden. Returns None if no suit chosen (only if not must_call).
    """
    counts = count_suits(hand)
    forbidden = upcard.suit
    for suit in SUITS:
        if suit == forbidden:
            continue
        if counts.get(suit, 0) >= 3:
            return suit
    if must_call:
        for suit in SUITS:
            if suit != forbidden:
                return suit
    return None


def choose_lead(hand, trump):
    """
    Choose a card to lead. Prefer right bower, then left bower, then high trump, then high off-suit.
    """
    if not hand:
        return None
    hand = list(hand)
    hand.sort(key=lambda c: -c.ordering_value(trump))
    return hand[0]


def get_valid_plays(hand, lead_card, trick, trump):
    """
    Return list of cards that are legal to play. Must follow lead suit (effective_suit) if possible.
    """
    if not trick:
        return list(hand)
    lead_suit = lead_card.effective_suit(trump)
    in_suit = [c for c in hand if c.effective_suit(trump) == lead_suit]
    if in_suit:
        return in_suit
    return list(hand)


def choose_follow(hand, lead_card, trick, trump):
    """
    Choose a card when following. Must follow suit if possible. Tries to beat current winner else plays lowest.
    """
    valid = get_valid_plays(hand, lead_card, trick, trump)
    if not valid:
        return None
    if len(valid) == 1:
        return valid[0]
    # Find current winning index in trick (by ordering_value in lead_suit/trump context)
    lead_suit = lead_card.effective_suit(trump)
    best_idx = 0
    best_val = trick[0].ordering_value(trump) if lead_suit == trick[0].effective_suit(trump) else -1
    for i, c in enumerate(trick[1:], 1):
        eff = c.effective_suit(trump)
        if eff != lead_suit:
            continue
        v = c.ordering_value(trump)
        if v > best_val:
            best_val = v
            best_idx = i
    winning_val = best_val
    # Try to play a card that beats winning_val (and is in valid)
    valid.sort(key=lambda c: -c.ordering_value(trump))
    for c in valid:
        if c.effective_suit(trump) == lead_suit and c.ordering_value(trump) > winning_val:
            return c
    # Can't beat: play lowest of valid
    valid.sort(key=lambda c: c.ordering_value(trump))
    return valid[0]


class Player:
    """Base player: name, seat index, hand."""

    def __init__(self, name, seat_index):
        self.name = name
        self.seat_index = seat_index
        self.hand = []

    def receive_hand(self, cards):
        self.hand = list(cards)

    def choose_pickup(self, upcard):
        raise NotImplementedError

    def choose_discard(self):
        raise NotImplementedError

    def call_trump(self, upcard, must_call):
        raise NotImplementedError

    def play_card(self, lead_card, trick, trump):
        raise NotImplementedError


class HumanPlayer(Player):
    """Human player: prompts via display."""

    def __init__(self, name, seat_index, display):
        super().__init__(name, seat_index)
        self._display = display

    def choose_pickup(self, upcard):
        print("Flipped up:")
        self._display.print_hand([upcard])
        print("\nYour hand:")
        self._display.print_hand(self.hand)
        print("")
        result = self._display.prompt_pickup_or_pass()
        return result == "pickup"

    def choose_discard(self, upcard=None):
        # Dealer has 5 cards; we're picking up upcard and discarding one of the 5 (hand never has 6)
        if upcard is not None:
            print("You're picking up the {} of {}.".format(upcard.rank, upcard.suit))
            print("")
        self._display.print_hand(self.hand)
        return self._display.prompt_discard(len(self.hand))

    def call_trump(self, upcard, must_call):
        self._display.print_hand(self.hand)
        return self._display.prompt_call_trump(upcard.suit)

    def play_card(self, lead_card, trick, trump):
        self._display.print_hand(self.hand)
        idx = self._display.prompt_play_card(len(self.hand))
        return self.hand[idx]


class BotPlayer(Player):
    """Bot with single strategy: pickup/call trump by suit count, lead/follow by ordering_value."""

    PICKUP_MESSAGES = (
        'Pick that shit up!',
        'Pick it up!',
        'Pick it up!',
    )
    PASS_MESSAGES = ('Fuck that, pass.', 'Pass.', 'Pass.')

    def __init__(self, name, seat_index, display=None):
        super().__init__(name, seat_index)
        self._display = display

    def _say(self, msg):
        if self._display:
            print('{}: "{}"'.format(self.name, msg))

    def choose_pickup(self, upcard):
        if want_pickup(self.hand, upcard):
            msg = self.PICKUP_MESSAGES[min(self.seat_index - 1, 2)] if self.seat_index > 0 else "Pick it up!"
            self._say(msg)
            return True
        self._say(self.PASS_MESSAGES[min(self.seat_index - 1, 2)] if self.seat_index > 0 else "Pass.")
        return False

    def choose_discard(self, upcard=None):
        # Dealer has 5 cards; pick lowest by rank to discard before adding upcard
        from .constants import RANK_ORDER
        worst = min(self.hand, key=lambda c: RANK_ORDER[c.rank])
        return self.hand.index(worst)

    def call_trump(self, upcard, must_call):
        suit = call_trump(self.hand, upcard, must_call)
        if suit:
            self._say(suit + "!")
        else:
            self._say("Pass.")
        return suit

    def play_card(self, lead_card, trick, trump):
        if not trick:
            card = choose_lead(self.hand, trump)
        else:
            card = choose_follow(self.hand, lead_card, trick, trump)
        if card is None:
            card = self.hand[0]
        return card
