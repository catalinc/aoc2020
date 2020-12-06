import re
import sys
import unittest
from collections import Counter
from typing import List


def parse_answers(s: str) -> List[List[str]]:
    ans = []
    for p in re.split(r"(?m)^\s*$\s*", s):
        ans.append(re.findall("[a-z]+", p))
    return ans


def count_one_yes(ans: List[List[str]]) -> int:
    cnt = 0
    for g in ans:
        qs = {a for p in g for a in p}
        cnt += len(qs)
    return cnt


def count_all_yes(ans: List[List[str]]):
    cnt = 0
    for g in ans:
        qs = Counter([a for p in g for a in p])
        for k in qs:
            if qs[k] == len(g):
                cnt += 1
    return cnt


def part1(ans: List[List[str]]) -> None:
    print(count_one_yes(ans))


def part2(ans: List[List[str]]) -> None:
    print(count_all_yes(ans))


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.input = """abc

a
b
c

ab
ac

a
a
a
a

b"""

    def test_parse_answers(self):
        ans = parse_answers(self.input)
        self.assertEqual(5, len(ans))
        self.assertEqual("abc", ans[0][0])
        self.assertEqual("ab", ans[2][0])
        self.assertEqual("b", ans[4][0])

    def test_count_one_yes(self):
        self.assertEqual(11, count_one_yes(parse_answers(self.input)))

    def test_count_all_yes(self):
        self.assertEqual(6, count_all_yes(parse_answers(self.input)))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            answers = parse_answers(infile.read())
            part1(answers)
            part2(answers)
    else:
        unittest.main()
