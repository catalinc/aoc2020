import re
import unittest

import sys


def check_passwd_old(s: str) -> bool:
    m = re.match(r"(\d+)-(\d+)\s(\w):\s(\w+)", s, re.ASCII)
    lo, hi, ch, pwd = int(m[1]), int(m[2]), m[3], m[4]
    cnt = 0
    for c in pwd:
        if c == ch:
            cnt += 1
    return lo <= cnt <= hi


def check_passwd_new(s: str) -> bool:
    m = re.match(r"(\d+)-(\d+)\s(\w):\s(\w+)", s, re.ASCII)
    fst, snd, ch, pwd = int(m[1]) - 1, int(m[2]) - 1, m[3], m[4]
    return (pwd[fst] == ch) ^ (pwd[snd] == ch)


def part1(entries):
    cnt = 0
    for p in entries:
        if check_passwd_old(p):
            cnt += 1
    print(cnt)


def part2(entries):
    cnt = 0
    for p in entries:
        if check_passwd_new(p):
            cnt += 1
    print(cnt)


class Test(unittest.TestCase):
    def test_check_password(self):
        data = [
            ("1-3 a: abcde", True),
            ("1-3 b: cdefg", False),
            ("2-9 c: ccccccccc", True),
        ]
        for p, v in data:
            self.assertEqual(v, check_passwd_old(p))

    def test_check_passwd_new(self):
        data = [
            ("1-3 a: abcde", True),
            ("1-3 b: cdefg", False),
            ("2-9 c: ccccccccc", False),
        ]
        for p, v in data:
            self.assertEqual(v, check_passwd_new(p))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as infile:
            lines = infile.readlines()
            part1(lines)
            part2(lines)
    else:
        unittest.main()
