import sys
import unittest

from typing import Tuple


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
    first, n = busses[0][0], len(busses)
    t = first
    while True:
        t += first
        i, found = 1, True
        while i < n:
            bus_id, offset = busses[i]
            if (t + offset) % bus_id != 0:
                found = False
                break
            i += 1
        if found:
            return t


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
