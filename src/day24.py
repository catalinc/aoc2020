import sys
import re
import unittest

from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class HexTile:
    x: int
    y: int
    z: int

    def __add__(self, other):
        return HexTile(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)


directions = {
    'w': HexTile(x=-1, y=1, z=0),
    'nw': HexTile(x=0, y=1, z=-1),
    'ne': HexTile(x=1, y=0, z=-1),
    'e': HexTile(x=1, y=-1, z=0),
    'se': HexTile(x=0, y=-1, z=1),
    'sw': HexTile(x=-1, y=0, z=1)
}


def tile_from_path(path: str) -> HexTile:
    coord = HexTile(x=0, y=0, z=0)
    for d in re.findall("w|nw|ne|e|se|sw", path):
        coord = coord + directions[d]
    return coord


def part1(paths: list[str]) -> set[HexTile]:
    black = set()
    for p in paths:
        t = tile_from_path(p)
        if t in black:
            black.remove(t)
        else:
            black.add(t)
    return black


def neighbours(tile: HexTile):
    for d in directions:
        yield tile + directions[d]


def count_black_neighbours(tile: HexTile, black_tiles: set[HexTile]) -> int:
    count = 0
    for n in neighbours(tile):
        if n in black_tiles:
            count += 1
    return count


def part2(paths: list[str], rounds: int) -> int:
    black_tiles = part1(paths)
    while rounds > 0:
        to_white, to_black = set(), set()
        for tile in black_tiles:
            count = count_black_neighbours(tile, black_tiles)
            if count == 0 or count > 2:
                to_white.add(tile)
            for neighbour in neighbours(tile):
                if neighbour not in black_tiles:
                    count = count_black_neighbours(neighbour, black_tiles)
                    if count == 2:
                        to_black.add(neighbour)
        for tile in to_white:
            black_tiles.remove(tile)
        for tile in to_black:
            black_tiles.add(tile)
        rounds -= 1
    return len(black_tiles)


class Test(unittest.TestCase):

    def setUp(self) -> None:
        s = """
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
"""
        self.paths = [p for p in s.split('\n') if p]

    def test_part1(self):
        self.assertEqual(10, len(part1(self.paths)))

    def test_part2(self):
        self.assertEqual(2208, part2(self.paths, 100))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            lines = [line for line in infile.read().split('\n') if line]
            print(len(part1(lines)))
            print(part2(lines, 100))
    else:
        unittest.main()
