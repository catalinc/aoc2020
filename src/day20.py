import re
import sys
import unittest


class Tile:
    def __init__(self, tile_id: int, rows: list[str]):
        self.id = tile_id
        self.rows = rows
        self.size = len(rows)

    def height(self) -> int:
        return len(self.rows)

    def width(self) -> int:
        return len(self.rows[0])

    def north_edge(self) -> str:
        return self.rows[0]

    def south_edge(self) -> str:
        return self.rows[-1]

    def east_edge(self) -> str:
        return ''.join(t[-1] for t in self.rows)

    def west_edge(self) -> str:
        return ''.join(t[0] for t in self.rows)

    def remove_border(self):
        result = []
        for i in range(1, self.size - 1):
            result.append(''.join([self.rows[i][j] for j in range(1, self.size - 1)]))
        self.rows = result

    def rotate_right(self):
        result = []
        for i in range(self.size):
            result.append(''.join([self.rows[self.size - j - 1][i] for j in range(self.size)]))
        self.rows = result

    def flip_up_down(self):
        result = []
        for t in reversed(self.rows):
            result.append(t)
        self.rows = result


def parse_tile(s: str) -> Tile:
    lines = s.split('\n')
    if m := re.match(r'Tile (\d+):', lines[0]):
        tile_id = int(m[1])
        rows = [line for line in lines[1:] if line]
        return Tile(tile_id, rows)


def parse_tiles(s) -> list[Tile]:
    tiles = []
    for section in re.split(r"(?m)^\s*$\s*", s):
        if section:
            tiles.append(parse_tile(section))
    return tiles


transform = [
    lambda tile: tile,
    lambda tile: tile.rotate_right(),
    lambda tile: tile.rotate_right(),
    lambda tile: tile.rotate_right(),
    lambda tile: tile.flip_up_down(),
    lambda tile: tile.rotate_right(),
    lambda tile: tile.rotate_right(),
    lambda tile: tile.rotate_right(),
]


def assemble(mosaic: list[Tile], visited: set[Tile], tiles: list[Tile], border_size: int) -> list[Tile]:
    if len(tiles) == len(mosaic):
        return mosaic
    for tile in tiles:
        if tile not in visited:
            for fn in transform:
                fn(tile)
                if fit(mosaic, tile, border_size):
                    solution = assemble(mosaic + [tile], visited.union({tile}), tiles, border_size)
                    if solution:
                        return solution


def fit(mosaic: list[Tile], tile: Tile, border_size: int) -> bool:
    if len(mosaic) + 1 - border_size > 0:
        if tile.north_edge() != mosaic[len(mosaic) - border_size].south_edge():
            return False
    if (len(mosaic) + 1) % border_size != 1:
        if tile.west_edge() != mosaic[len(mosaic) - 1].east_edge():
            return False
    return True


def checksum(tiles: list[Tile]) -> int:
    mosaic_size, border_size = len(tiles), int(len(tiles) ** 0.5)
    mosaic = assemble([], set(), tiles, border_size)
    return mosaic[0].id * mosaic[(border_size - 1)].id * mosaic[(mosaic_size - border_size)].id * mosaic[
        (mosaic_size - 1)].id


def part1(tiles: list[Tile]):
    print(checksum(tiles))


def to_picture(mosaic: list[Tile]) -> Tile:
    tiles_area_no_border, tile_size = mosaic[0].size - 2, int(len(mosaic) ** 0.5)
    picture_size = tiles_area_no_border * tile_size
    picture = ['' for _ in range(picture_size)]
    for i, tile in enumerate(mosaic):
        tile.remove_border()
        for j, t in enumerate(tile.rows):
            picture[(i // tile_size) * tiles_area_no_border + j] += t
    return Tile(0, picture)


def count_occurrences(shape: list[str], tile: Tile) -> int:
    shape_height = len(shape)
    shape_width = len(shape[0])
    for fn in transform:
        fn(tile)
        count = 0
        for i in range(0, tile.height() - shape_height + 1):
            for j in range(0, tile.width() - shape_width + 1):
                found = True
                for p in range(shape_height):
                    for q in range(shape_width):
                        if (shape[p][q] != ' ') and (shape[p][q] != tile.rows[i + p][j + q]):
                            found = False
                if found:
                    count += 1
        if count:
            return count
    return 0


def water_roughness(tiles: list[Tile]) -> int:
    mosaic_size, border_size = len(tiles), int(len(tiles) ** 0.5)
    picture = to_picture(assemble([], set(), tiles, border_size))
    monster = [
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   ',
    ]
    return count_occurrences(['#'], picture) - count_occurrences(monster, picture) * 15


def part2(tiles: list[Tile]):
    print(water_roughness(tiles))


class Test(unittest.TestCase):

    def setUp(self):
        s = """
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""
        self.tiles = parse_tiles(s)

    def test_parse_tile(self):
        s = """Tile 3389:
....#..#.#
##...#....
.....#....
.....#..#.
.#...##...
##..#...##
##.##..#..
#...##....
.#....#...
..#......."""
        tile = parse_tile(s)
        self.assertEqual(3389, tile.id)
        self.assertEqual(10, tile.size)
        self.assertEqual('.', tile.rows[0][0])
        self.assertEqual('#', tile.rows[0][4])

    def test_checksum(self):
        self.assertEqual(20899048083289, checksum(self.tiles))

    def test_water_roughness(self):
        self.assertEqual(273, water_roughness(self.tiles))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            satellite_data = infile.read()
            part1(parse_tiles(satellite_data))
            part2(parse_tiles(satellite_data))
    else:
        unittest.main()
