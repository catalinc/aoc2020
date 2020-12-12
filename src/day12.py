import math
import sys
import unittest

from typing import List


class Waypoint:

    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.angle = 0

    def rotate(self, degrees):
        self.angle += degrees
        rad = math.radians(degrees)
        x, y = self.dx, self.dy
        self.dx = x * int(math.cos(rad)) - y * int(math.sin(rad))
        self.dy = x * int(math.sin(rad)) + y * int(math.cos(rad))

    def __str__(self):
        return f"dx={self.dx}, dy={self.dy}, angle={self.angle}"


class Ship:

    def __init__(self, wp: Waypoint = None):
        self.angle = 0
        self.x = 0
        self.y = 0
        self.wp = wp

    def navigate(self, cmd: str) -> None:
        act, val = cmd[0], int(cmd[1:])
        if act == 'N':
            if self.wp:
                self.wp.dy += val
            else:
                self.y += val
        elif act == 'S':
            if self.wp:
                self.wp.dy -= val
            else:
                self.y -= val
        elif act == 'E':
            if self.wp:
                self.wp.dx += val
            else:
                self.x += val
        elif act == 'W':
            if self.wp:
                self.wp.dx -= val
            else:
                self.x -= val
        elif act == 'L':
            if self.wp:
                self.wp.rotate(val)
                pass
            else:
                self.angle += val
        elif act == 'R':
            if self.wp:
                self.wp.rotate(-val)
            else:
                self.angle -= val
        elif act == 'F':
            if self.wp:
                self.x = self.x + val * self.wp.dx
                self.y = self.y + val * self.wp.dy
            else:
                rad = math.radians(self.angle)
                self.x = self.x + val * int(math.cos(rad))
                self.y = self.y + val * int(math.sin(rad))

    def manhattan_dist_from_origin(self) -> int:
        return abs(self.x) + abs(self.y)

    def __str__(self):
        return f"x={self.x}, y={self.y}, angle={self.angle}, wp={self.wp}"


def part1(plan: List[str]) -> None:
    ship = Ship()
    for cmd in plan:
        ship.navigate(cmd)
    print(ship.manhattan_dist_from_origin())


def part2(plan: List[str]) -> None:
    ship = Ship(wp=Waypoint(10, 1))
    for cmd in plan:
        ship.navigate(cmd)
    print(ship.manhattan_dist_from_origin())


class Test(unittest.TestCase):

    def test_navigate(self):
        ship = Ship()
        for cmd in ('F10', 'N3', 'F7', 'R90', 'F11'):
            ship.navigate(cmd)
        self.assertEqual(17, ship.x)
        self.assertEqual(-8, ship.y)
        self.assertEqual(25, ship.manhattan_dist_from_origin())

    def test_navigate_with_waypoint(self):
        ship = Ship(wp=Waypoint(10, 1))
        for cmd in ('F10', 'N3', 'F7', 'R90', 'F11'):
            ship.navigate(cmd)
        self.assertEqual(214, ship.x)
        self.assertEqual(-72, ship.y)
        self.assertEqual(286, ship.manhattan_dist_from_origin())


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            lines = [s for s in infile.read().split('\n') if s]
            part1(lines)
            part2(lines)
    else:
        unittest.main()
