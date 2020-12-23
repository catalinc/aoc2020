import sys
import unittest

from collections import deque


def part1(game_data: str):
    deck_p1, deck_p2 = parse_input(game_data)
    print(combat(deck_p1, deck_p2))


def parse_input(game_data: str) -> tuple[deque[int], deque[int]]:
    lines = [line for line in game_data.split('\n') if line]
    deck_p1, deck_p2, crt_deck = deque([]), deque([]), None
    for line in lines:
        if line.startswith("Player 1"):
            crt_deck = deck_p1
            continue
        if line.startswith("Player 2"):
            crt_deck = deck_p2
            continue
        crt_deck.append(int(line))
    return deck_p1, deck_p2


def combat(deck_p1: deque[int], deck_p2: deque[int]) -> int:
    while deck_p1 and deck_p2:
        top_p1 = deck_p1.popleft()
        top_p2 = deck_p2.popleft()
        if top_p1 > top_p2:
            winner = deck_p1
        else:
            winner = deck_p2
        winner.append(max(top_p1, top_p2))
        winner.append(min(top_p1, top_p2))
    if deck_p1:
        return score(deck_p1)
    else:
        return score(deck_p2)


def score(deck: deque[int]) -> int:
    total, m = 0, 1
    for n in reversed(deck):
        total += n * m
        m += 1
    return total


def part2(game_data: str):
    deck_p1, deck_p2 = parse_input(game_data)
    p1 = Player('p1', deck_p1)
    p2 = Player('p2', deck_p2)
    winner = rec_combat(p1, p2)
    print(score(winner.deck))


class Player:

    def __init__(self, name: str, deck: deque[int]):
        self.name = name
        self.deck = deck

    def copy(self, count: int):
        new_deck = deque([])
        for i in range(count):
            new_deck.append(self.deck[i])
        return Player(self.name, new_deck)


def rec_combat(p1: Player, p2: Player) -> Player:
    hist = set()
    while p1.deck and p2.deck:
        state = (tuple(p1.deck), tuple(p2.deck))
        if state in hist:
            return p1
        hist.add(state)
        top_p1 = p1.deck.popleft()
        top_p2 = p2.deck.popleft()
        if len(p1.deck) >= top_p1 and len(p2.deck) >= top_p2:
            winner = rec_combat(p1.copy(top_p1), p2.copy(top_p2))
        else:
            if top_p1 > top_p2:
                winner = p1
            else:
                winner = p2
        if winner.name == p1.name:
            p1.deck.append(top_p1)
            p1.deck.append(top_p2)
        else:
            p2.deck.append(top_p2)
            p2.deck.append(top_p1)
    if p1.deck:
        return p1
    return p2


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.input = """
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

    def test_combat(self):
        deck_p1, deck_p2 = parse_input(self.input)
        self.assertEqual(306, combat(deck_p1, deck_p2))

    def test_rec_combat(self):
        deck_p1, deck_p2 = parse_input(self.input)
        p1 = Player('p1', deck_p1)
        p2 = Player('p2', deck_p2)
        winner = rec_combat(p1, p2)
        self.assertEqual('p2', winner.name)
        self.assertEqual(291, score(winner.deck))

    def test_rec_combat_loop(self):
        gs = """
Player 1:
43
19

Player 2:
2
29
14"""
        deck_p1, deck_p2 = parse_input(gs)
        p1 = Player('p1', deck_p1)
        p2 = Player('p2', deck_p2)
        winner = rec_combat(p1, p2)
        self.assertTrue(winner)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            s = infile.read()
            part1(s)
            part2(s)
    else:
        unittest.main()
