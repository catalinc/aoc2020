import sys
import unittest

from typing import Iterable


def seat_id(ticket: str) -> int:
    lo, hi = 0, 127
    for i in range(7):
        mid = (lo + hi) // 2
        if ticket[i] == 'F':
            hi = mid
        else:
            lo = mid + 1
    row = lo
    lo, hi = 0, 7
    for i in range(7, len(ticket)):
        mid = (lo + hi) // 2
        if ticket[i] == 'L':
            hi = mid
        else:
            lo = mid + 1
    col = lo
    return row * 8 + col


def part1(tickets: Iterable[str]) -> None:
    best = -1
    for s in tickets:
        sid = seat_id(s)
        best = max(best, sid)
    print(best)


def part2(tickets: Iterable[str]) -> None:
    seats = [seat_id(s) for s in tickets]
    seats.sort()
    for i in range(len(seats) - 1):
        crt = seats[i]
        nxt = seats[i + 1]
        if nxt - crt == 2:
            print(crt + 1)
            break


class Test(unittest.TestCase):

    def test_seat_id(self):
        data = [('FBFBBFFRLR', 357),
                ('BFFFBBFRRR', 567),
                ('FFFBBBFRRR', 119),
                ('BBFFBBFRLL', 820)]
        for s, sid in data:
            self.assertEqual(sid, seat_id(s), f"failed for: {s}")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            entries = infile.read().split()
            part1(entries)
            part2(entries)
    else:
        unittest.main()
