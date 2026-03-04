"""Game state and flow: ordering phase, play phase, trick resolution."""

import time

from .constants import CARDS_PER_HAND, NUM_PLAYERS
from .deck import Deck


def winner_of_trick(trick, trump):
    """
    Return the index (0-3) of the winning card in trick. trick is list of 4 cards in play order.
    """
    lead_suit = trick[0].effective_suit(trump)
    # Cards that count as trump (including left bower)
    trump_indices = [i for i, c in enumerate(trick) if c.effective_suit(trump) == trump]
    if trump_indices:
        best_i = max(trump_indices, key=lambda i: trick[i].ordering_value(trump))
        return best_i
    # No trump: follow suit wins (lead_suit); all should have followed
    in_suit_indices = [i for i, c in enumerate(trick) if c.effective_suit(trump) == lead_suit]
    if not in_suit_indices:
        return 0
    best_i = max(in_suit_indices, key=lambda i: trick[i].ordering_value(trump))
    return best_i


class EuchreGame:
    """
    One round: deal, ordering phase (pick up or pass, then call trump), then 5 tricks.
    Players are in seat order: 0 = human (by convention), 1,2,3 = bots. Dealer and leader are indices.
    """

    def __init__(self, players, display=None):
        assert len(players) == NUM_PLAYERS
        self.players = players
        if display is None:
            from . import display as _disp
            self.display = _disp
        else:
            self.display = display
        self.deck = Deck()
        self.kitty = []
        self.trump = None
        self.dealer_index = 0
        self.leader_index = 0
        self.current_trick = []
        self.trick_winners = []

    def _clear_screen(self):
        self.display.clear_screen()

    def _deal(self):
        self.deck.shuffle()
        hands, self.kitty = self.deck.deal()
        for i, p in enumerate(self.players):
            p.receive_hand(hands[i])

    def _player_index_to_seat(self, index):
        """Order of play: (dealer+1), (dealer+2), (dealer+3), dealer."""
        return (self.dealer_index + 1 + index) % NUM_PLAYERS

    def _ordering_phase(self):
        """Flip upcard, go around for pickup; if pass-all, go around for call. Set trump and optionally give dealer upcard."""
        self._clear_screen()
        print("Shuffling cards...")
        self._deal()
        self._clear_screen()
        print("Cards have been shuffled!")
        time.sleep(0.5)
        self._clear_screen()
        print("Dealing...")
        time.sleep(0.3)
        self._clear_screen()

        upcard = self.kitty[0]
        print(self.display.card_image(upcard))
        print("{} of {} has been flipped up!".format(upcard.rank, upcard.suit))
        print("\n\n")

        pickup = False
        # First round: who wants to order up? (dealer+1, dealer+2, dealer+3, dealer)
        for i in range(NUM_PLAYERS):
            seat = (self.dealer_index + 1 + i) % NUM_PLAYERS
            p = self.players[seat]
            print("{} is choosing...".format(p.name))
            if p.choose_pickup(upcard):
                pickup = True
                self.trump = upcard.suit
                break
            print("\n\n")

        if not pickup:
            # Second round: call a suit (same order); dealer must call if all pass
            for i in range(NUM_PLAYERS):
                seat = (self.dealer_index + 1 + i) % NUM_PLAYERS
                p = self.players[seat]
                print("{} is choosing...".format(p.name))
                must_call = seat == self.dealer_index and i == NUM_PLAYERS - 1
                if must_call:
                    print("Looks like {} has to call!".format(p.name))
                    print("")
                suit = p.call_trump(upcard, must_call=must_call)
                if suit:
                    self.trump = suit
                    break
                print("\n\n")
            if not self.trump:
                # Stuck: force dealer to call (shouldn't happen if must_call worked)
                self.trump = self.players[self.dealer_index].call_trump(upcard, must_call=True) or upcard.suit

            self._clear_screen()
        else:
            # Dealer picks up upcard: choose which of 5 cards to discard, then replace it with upcard (hand stays 5 cards)
            dealer = self.players[self.dealer_index]
            discard_idx = dealer.choose_discard(upcard)
            dealer.hand.pop(discard_idx)
            dealer.hand.append(upcard)
            if dealer.seat_index == 0:
                print("\nYour new hand:")
                self.display.print_hand(dealer.hand)

        assert self.trump

    def _play_one_trick(self):
        """One trick: each player plays in order (leader first). Returns winner seat index."""
        self.current_trick = []
        trick_by_seat = [None] * NUM_PLAYERS
        order = [
            (self.leader_index + i) % NUM_PLAYERS
            for i in range(NUM_PLAYERS)
        ]
        player_names = [p.name for p in self.players]

        # Show empty table and user's hand at start of trick
        self._clear_screen()
        human_hand = list(self.players[0].hand) if self.players[0].hand else None
        self.display.print_table(trick_by_seat, player_names, human_hand=human_hand)
        print("")

        lead_card = None
        for seat in order:
            p = self.players[seat]
            print("{}'s turn...".format(p.name))
            time.sleep(0.3)
            # Show table (user's hand only at start of trick; when it's human's turn, play_card will show hand and prompt)
            self._clear_screen()
            self.display.print_table(trick_by_seat, player_names, human_hand=None)
            print("")
            card = p.play_card(lead_card, list(self.current_trick), self.trump)
            p.hand.remove(card)
            if lead_card is None:
                lead_card = card
            self.current_trick.append(card)
            trick_by_seat[seat] = card
            # Redraw table with the new card in place
            self._clear_screen()
            self.display.print_table(trick_by_seat, player_names, human_hand=None)
            print("")
            print("{} plays.".format(p.name))
            time.sleep(0.5)

        win_offset = winner_of_trick(self.current_trick, self.trump)
        winner_seat = order[win_offset]
        self.trick_winners.append(winner_seat)
        self.leader_index = winner_seat
        print("{} wins the trick.".format(self.players[winner_seat].name))
        time.sleep(1.0)
        return winner_seat

    def play_phase(self):
        """Play 5 tricks. First leader is left of dealer."""
        self.leader_index = (self.dealer_index + 1) % NUM_PLAYERS
        for t in range(5):
            self._play_one_trick()
            print("Trick {} complete.\n".format(t + 1))

    def run(self):
        """Run one full round: ordering then 5 tricks."""
        self._ordering_phase()
        self.play_phase()
