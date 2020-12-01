import sys
import unittest
from typing import Tuple, Iterable, Sequence


def two_sum(nums: Iterable[int], n: int) -> Tuple[int, int]:
    seen = set()
    for x in nums:
        r = n - x
        if r in seen:
            return x, r
        seen.add(x)


def read_ints(fname: str) -> Iterable[int]:
    with open(fname) as infile:
        for line in infile:
            yield int(line)


def three_sum(nums: Sequence[int], n: int) -> Tuple[int, int, int]:
    for i in range(0, len(nums) - 2):
        a = nums[i]
        for j in range(i + 1, len(nums) - 1):
            b = nums[j]
            for k in range(j + 1, len(nums)):
                c = nums[k]
                if a + b + c == n:
                    return a, b, c


def part1(nums: Iterable[int], n: int):
    a, b = two_sum(nums, n)
    print(a * b)


def part2(nums: Sequence[int], n: int):
    a, b, c = three_sum(nums, n)
    print(a * b * c)


class Test(unittest.TestCase):

    def test_two_sum(self):
        self.assertEqual((299, 1721), two_sum([1721, 979, 366, 299, 675, 1456], 2020))

    def test_three_sum(self):
        self.assertEqual((979, 366, 675), three_sum([1721, 979, 366, 299, 675, 1456], 2020))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        data = list(read_ints(sys.argv[1]))
        part1(data, 2020)
        part2(data, 2020)
    else:
        unittest.main()
