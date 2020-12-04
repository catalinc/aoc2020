import unittest
from typing import List

import sys


def count_trees(grid: List[List[str]], right: int, down: int) -> int:
    w, h, r, c, cnt = len(grid[0]), len(grid), 0, 0, 0
    while r < h:
        if grid[r][c] == '#':
            cnt += 1
        c = (c + right) % w
        r = r + down
    return cnt


def parse_grid(s: str) -> List[List[str]]:
    return [list(r) for r in s.split('\n') if r]


def part1(grid):
    print(count_trees(grid, 3, 1))


def part2(grid):
    p = 1
    for right, down in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        p *= count_trees(grid, right, down)
    print(p)


class Test(unittest.TestCase):

    def test_count_trees(self):
        grid = parse_grid("""..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#""")
        data = [(1, 1, 2), (3, 1, 7), (5, 1, 3), (7, 1, 4), (1, 2, 2)]
        for r, d, t in data:
            self.assertEqual(t, count_trees(grid, r, d))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            g = parse_grid(infile.read())
            part1(g)
            part2(g)
    else:
        unittest.main()
