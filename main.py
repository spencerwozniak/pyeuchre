"""Entry point for Euchre: banner, player name, run one round."""

from euchre import display
from euchre import BotPlayer, EuchreGame, HumanPlayer


def main():
    display.print_banner()
    name = display.prompt_player_name()
    human = HumanPlayer(name, 0, display)
    bots = [
        BotPlayer("Player 1", 1),
        BotPlayer("Player 2", 2),
        BotPlayer("Player 3", 3),
    ]
    players = [human] + bots
    game = EuchreGame(players)
    game.run()


if __name__ == "__main__":
    main()
