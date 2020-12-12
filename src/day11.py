import sys
import unittest

from typing import List


def parse_grid(s: str) -> List[List[str]]:
    return [list(r) for r in s.split('\n') if r]


def simulate(grid: List[List[str]], count_occupied_fn, max_occupied: int) -> int:
    w, h = len(grid[0]), len(grid)
    while True:
        to_seat, to_clear = [], []
        for r in range(h):
            for c in range(w):
                occupied = count_occupied_fn(r, c, grid)
                seat = grid[r][c]
                if seat == 'L' and occupied == 0:
                    to_seat.append((r, c))
                elif seat == '#' and occupied >= max_occupied:
                    to_clear.append((r, c))
        if not to_seat and not to_clear:
            occupied = 0
            for r in range(h):
                for c in range(w):
                    if grid[r][c] == '#':
                        occupied += 1
            return occupied
        else:
            for r, c in to_seat:
                grid[r][c] = '#'
            for r, c in to_clear:
                grid[r][c] = 'L'


def count_occupied_adj(r: int, c: int, grid: List[List[str]]) -> int:
    w, h, cnt = len(grid[0]), len(grid), 0
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if i == 0 and j == 0:
                continue
            nr, nc = r + i, c + j
            if 0 <= nr < h and 0 <= nc < w:
                if grid[nr][nc] == '#':
                    cnt += 1
    return cnt


def count_occupied_vis(r: int, c: int, grid: List[List[str]]) -> int:
    w, h, cnt = len(grid[0]), len(grid), 0
    # N
    for i in range(r - 1, -1, -1):
        if grid[i][c] == 'L':
            break
        if grid[i][c] == '#':
            cnt += 1
            break
    # S
    for i in range(r + 1, h):
        if grid[i][c] == 'L':
            break
        if grid[i][c] == '#':
            cnt += 1
            break
    # W
    for i in range(c - 1, -1, -1):
        if grid[r][i] == 'L':
            break
        if grid[r][i] == '#':
            cnt += 1
            break
    # E
    for i in range(c + 1, w):
        if grid[r][i] == 'L':
            break
        if grid[r][i] == '#':
            cnt += 1
            break
    # NW
    i, j = r - 1, c - 1
    while i >= 0 and j >= 0:
        if grid[i][j] == 'L':
            break
        if grid[i][j] == '#':
            cnt += 1
            break
        i -= 1
        j -= 1
    # SE
    i, j = r + 1, c + 1
    while i < h and j < w:
        if grid[i][j] == 'L':
            break
        if grid[i][j] == '#':
            cnt += 1
            break
        i += 1
        j += 1
    # NE
    i, j = r - 1, c + 1
    while i >= 0 and j < w:
        if grid[i][j] == 'L':
            break
        if grid[i][j] == '#':
            cnt += 1
            break
        i -= 1
        j += 1
    # SW
    i, j = r + 1, c - 1
    while i < h and j >= 0:
        if grid[i][j] == 'L':
            break
        if grid[i][j] == '#':
            cnt += 1
            break
        i += 1
        j -= 1
    return cnt


def part1(grid: List[List[str]]) -> None:
    print(simulate(grid, count_occupied_adj, 4))


def part2(grid: List[List[str]]) -> None:
    print(simulate(grid, count_occupied_vis, 5))


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.grid = parse_grid("""
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""")

    def test_simulate_occupied_adj(self):
        self.assertEqual(37, simulate(self.grid, count_occupied_adj, 4))

    def test_count_occupied_vis(self):
        grid = parse_grid("""
.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....""")
        self.assertEqual(8, count_occupied_vis(4, 3, grid))

        grid = parse_grid("""
.............
.L.L.#.#.#.#.
.............""")
        self.assertEqual(0, count_occupied_vis(1, 1, grid))

        grid = parse_grid("""
.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.""")
        self.assertEqual(0, count_occupied_vis(3, 3, grid))

    def test_simulate_occupied_vis(self):
        self.assertEqual(26, simulate(self.grid, count_occupied_vis, 5))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            s = infile.read()
            part1(parse_grid(s))
            part2(parse_grid(s))
    else:
        unittest.main()
