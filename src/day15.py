import sys
import unittest
from typing import List
from collections import defaultdict


def elf_game(start_nums: List[int], max_turns: int) -> int:
    hist = defaultdict(list)
    for i, n in enumerate(start_nums):
        hist[n].append(i + 1)
    last = start_nums[-1]
    turn = len(start_nums)
    while turn < max_turns:
        turn += 1
        spoken = 0
        age = hist[last]
        if len(age) > 1:
            spoken = age[-1] - age[-2]
        hist[spoken].append(turn)
        last = spoken
    return last


def part1() -> None:
    print(elf_game([5, 1, 9, 18, 13, 8, 0], 2020))


def part2() -> None:
    print(elf_game([5, 1, 9, 18, 13, 8, 0], 30000000))


class Test(unittest.TestCase):

    def test_elf_game(self):
        test_data = [
            ([0, 3, 6], 10, 0),
            ([0, 3, 6], 2020, 436),
            ([1, 3, 2], 2020, 1),
            ([2, 1, 3], 2020, 10),
            ([1, 2, 3], 2020, 27),
            ([2, 3, 1], 2020, 78),
            ([3, 2, 1], 2020, 438),
            ([3, 1, 2], 2020, 1836),
        ]
        for ns, t, n in test_data:
            self.assertEqual(n, elf_game(ns, t), f"({ns}, {t})")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        part1()
        part2()
    else:
        unittest.main()
