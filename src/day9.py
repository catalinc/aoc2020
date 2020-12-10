import unittest
from typing import List

import sys


def find_first_invalid(nums: List[int], k: int) -> int:
    for i in range(k, len(nums)):
        n, prev, ok = nums[i], set(nums[i - k: i]), False
        for p in prev:
            d = n - p
            if d in prev and d != p:
                ok = True
                break
        if not ok:
            return n


def find_subarray_sum(nums: List[int], k: int) -> List[int]:
    i, start, crt_sum = 1, 0, nums[0]
    while i < len(nums):
        while crt_sum > k and start < i - 1:
            crt_sum -= nums[start]
            start += 1
        if crt_sum == k:
            return nums[start: i]
        crt_sum += nums[i]
        i += 1


def part1(nums: List[int]) -> None:
    print(find_first_invalid(nums, 25))


def part2(nums: List[int]) -> None:
    arr = find_subarray_sum(nums, 20874512)
    print(min(arr) + max(arr))


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.data = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95,
                     102, 117, 150, 182, 127, 219, 299, 277, 309, 576]

    def test_find_first_invalid(self):
        self.assertEqual(127, find_first_invalid(self.data, 5))

    def test_find_subarray_sum(self):
        self.assertEqual([15, 25, 47, 40], find_subarray_sum(self.data, 127))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            ns = [int(s) for s in infile.read().split('\n') if s]
            part1(ns)
            part2(ns)
    else:
        unittest.main()
