import sys
import unittest
from collections import namedtuple
from typing import List, Dict, Set, Tuple

Cube = namedtuple("Cube", ["x", "y", "z"])

Grid3D = Set[Cube]


def part1(s: str) -> None:
    grid = parse_grid3d(s)
    for _ in range(6):
        grid = boot_cycle3d(grid)
    print(len(grid))


def parse_grid3d(s: str) -> Grid3D:
    grid = set()
    state = [[x for x in line] for line in s.split('\n') if line]
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == '#':
                grid.add(Cube(x=j, y=i, z=0))
    return grid


def boot_cycle3d(grid: Grid3D) -> Grid3D:
    min_x = min((c.x for c in grid)) - 1
    max_x = max((c.x for c in grid)) + 1
    min_y = min((c.y for c in grid)) - 1
    max_y = max((c.y for c in grid)) + 1
    min_z = min((c.z for c in grid)) - 1
    max_z = max((c.z for c in grid)) + 1
    new_grid = set()
    for z in range(min_z, max_z + 1):
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                cube = Cube(x, y, z)
                adjacent = neighbours3d(cube)
                active = 0
                for c in adjacent:
                    if c in grid:
                        active += 1
                if cube in grid:
                    if active in (2, 3):
                        new_grid.add(cube)
                else:
                    if active == 3:
                        new_grid.add(cube)
    return new_grid


def neighbours3d(cube: Cube) -> List[Cube]:
    cubes = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                if dx == dy == dz == 0:
                    continue
                cubes.append(Cube(cube.x + dx, cube.y + dy, cube.z + dz))
    return cubes


HyperCube = namedtuple("HyperCube", ["x", "y", "z", "w"])

Grid4D = Set[HyperCube]


def part2(s: str) -> None:
    grid = parse_grid4d(s)
    for _ in range(6):
        grid = boot_cycle4d(grid)
    print(len(grid))


def parse_grid4d(s: str) -> Grid3D:
    grid = set()
    state = [[x for x in line] for line in s.split('\n') if line]
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == '#':
                grid.add(HyperCube(x=j, y=i, z=0, w=0))
    return grid


def boot_cycle4d(grid: Grid4D) -> Grid4D:
    min_x = min((c.x for c in grid)) - 1
    max_x = max((c.x for c in grid)) + 1
    min_y = min((c.y for c in grid)) - 1
    max_y = max((c.y for c in grid)) + 1
    min_z = min((c.z for c in grid)) - 1
    max_z = max((c.z for c in grid)) + 1
    min_w = min((c.w for c in grid)) - 1
    max_w = max((c.w for c in grid)) + 1
    new_grid = set()
    for w in range(min_w, max_w + 1):
        for z in range(min_z, max_z + 1):
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    cube = HyperCube(x, y, z, w)
                    adjacent = neighbours4d(cube)
                    active = 0
                    for c in adjacent:
                        if c in grid:
                            active += 1
                    if cube in grid:
                        if active in (2, 3):
                            new_grid.add(cube)
                    else:
                        if active == 3:
                            new_grid.add(cube)
    return new_grid


def neighbours4d(cube: HyperCube) -> List[HyperCube]:
    cubes = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for dw in (-1, 0, 1):
                    if dx == dy == dz == dw == 0:
                        continue
                    cubes.append(HyperCube(cube.x + dx, cube.y + dy, cube.z + dz, cube.w + dw))
    return cubes


class Test(unittest.TestCase):

    def test_boot_cycle3d(self):
        s = """.#.
..#
###"""
        grid = parse_grid3d(s)
        for _ in range(6):
            grid = boot_cycle3d(grid)
        self.assertEqual(112, len(grid))

    def test_boot_cycle4d(self):
        s = """.#.
..#
###"""
        grid = parse_grid4d(s)
        for _ in range(6):
            grid = boot_cycle4d(grid)
        self.assertEqual(848, len(grid))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            spec = infile.read()
            part1(spec)
            part2(spec)
    else:
        unittest.main()
