import unittest
from typing import Tuple, List

import sys


def first_bus_and_wait_time(depart: str, timetable: str) -> Tuple[int, int]:
    depart = int(depart)
    busses = [int(s) for s in timetable.split(',') if s and s != 'x']
    t = depart + 1
    while True:
        for i in busses:
            if t % i == 0:
                return i, t - depart
        t += 1


def part1(depart, timetable) -> None:
    i, t = first_bus_and_wait_time(depart, timetable)
    print(i * t)


def earliest_timestamp(timetable: str) -> int:
    busses = [(int(x), i) for i, x in enumerate(timetable.split(',')) if x != 'x']
    ns = [b[0] for b in busses]
    rs = [b[0] - b[1] for b in busses]
    return crt(ns, rs)


def crt(ns: List[int], rs: List[int]) -> int:
    m = 1
    for n in ns:
        m *= n
    ys = [m // n for n in ns]
    zs = [modinv(y, n) for y, n in zip(ys, ns)]
    x = sum([r * y * z for r, y, z in zip(rs, ys, zs)])
    return x % m


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a: int, m: int) -> int:
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def part2(timetable: str) -> None:
    print(earliest_timestamp(timetable))


class Test(unittest.TestCase):

    def test_first_bus_and_wait_time(self):
        self.assertEqual((59, 5), first_bus_and_wait_time('939', '7,13,x,x,59,x,31,19'))

    def test_earliest_timestamp(self):
        test_data = [
            ('7,13,x,x,59,x,31,19', 1068781),
            ('17,x,13,19', 3417),
            ('67,7,59,61', 754018),
            ('67,x,7,59,61', 779210),
            ('67,7,x,59,61', 1261476),
            ('1789,37,47,1889', 1202161486)
        ]
        for s, t in test_data:
            self.assertEqual(t, earliest_timestamp(s), s)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with (open(sys.argv[1], 'r')) as infile:
            ts = int(infile.readline())
            tt = infile.readline()
            part1(ts, tt)
            part2(tt)
    else:
        unittest.main()
