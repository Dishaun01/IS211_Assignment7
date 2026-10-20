"""Multiplayer Pig game for IS211 Assignment 7, including extra credit.

Run with: python pig.py
Or: python pig.py --numPlayers 3
Enter r to roll or h to hold. No third-party packages are required.
"""

import argparse
import random


class Die:
    """A six-sided die with a repeatable sequence of rolls."""

    def __init__(self):
        self.random = random.Random(0)

    def roll(self):
        return self.random.randint(1, 6)


class Player:
    """Store one player's name and banked score."""

    def __init__(self, name):
        self.name = name
        self.score = 0

    def hold(self, turn_total):
        self.score += turn_total

    def get_decision(self):
        return input("Roll (r) or hold (h)? ").strip().lower()


class PigGame:
    """Manage turn totals, player changes, and the winning score."""

    def __init__(self, num_players=2):
        if num_players < 2:
            raise ValueError("At least two players are required.")
        self.players = [Player(f"Player {number}")
                        for number in range(1, num_players + 1)]
        self.reset()

    def reset(self):
        """Start a fresh game, including scores and the seeded die."""
        for player in self.players:
            player.score = 0
        self.die = Die()
        self.current_player = 0
        self.turn_total = 0
        self.last_roll = None

    def show_status(self):
        player = self.players[self.current_player]
        rolled = "None this turn" if self.last_roll is None else self.last_roll
        print(f"\n{player.name} | Last roll: {rolled}")
        print(f"Turn total: {self.turn_total} | Game total: {player.score}")
        print("Scores: " + " | ".join(
            f"{person.name}: {person.score}" for person in self.players
        ))

    def next_turn(self):
        self.turn_total = 0
        self.last_roll = None
        self.current_player = (self.current_player + 1) % len(self.players)

    def play(self):
        print(f"Welcome to Pig! {len(self.players)} players race to 100 banked points.")
        print("Rolling 1 loses the turn total. Hold to bank your points.")
        while True:
            player = self.players[self.current_player]
            self.show_status()
            decision = player.get_decision()

            if decision == "r":
                self.last_roll = self.die.roll()
                print(f"{player.name} rolled {self.last_roll}.")
                if self.last_roll == 1:
                    self.turn_total = 0
                    self.show_status()
                    print("Pig out! No points banked. Your turn ends.")
                    self.next_turn()
                else:
                    self.turn_total += self.last_roll
            elif decision == "h":
                points = self.turn_total
                player.hold(points)
                self.turn_total = 0
                print(f"{player.name} banks {points} points.")
                self.show_status()
                if player.score >= 100:
                    print(f"\n{player.name} wins with {player.score} points!")
                    return
                self.next_turn()
            else:
                print("Invalid choice. Enter r to roll or h to hold.")


def main():
    """Read the player count and offer fresh games after each winner."""
    parser = argparse.ArgumentParser(description="Play Pig with human players.")
    parser.add_argument("--numPlayers", type=int, default=2,
                        help="number of human players (at least 2; default: 2)")
    args = parser.parse_args()
    if args.numPlayers < 2:
        parser.error("--numPlayers must be at least 2")
    game = PigGame(args.numPlayers)
    try:
        while True:
            game.play()
            while True:
                again = input("Play another game (y/n)? ").strip().lower()
                if again in ("y", "n"):
                    break
                print("Invalid choice. Enter y or n.")
            if again == "n":
                print("Thanks for playing!")
                return
            game.reset()
    except (EOFError, KeyboardInterrupt):
        print("\nGame ended.")


if __name__ == "__main__":
    main()
