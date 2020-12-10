import sys
import unittest
from typing import List, Tuple, Set, Dict


def find_distribution(jolts: List[int]) -> Tuple[int, int]:
    ones, threes = 0, 0
    jolts = jolts[:]
    jolts.append(0)
    jolts.sort()
    jolts.append(jolts[-1] + 3)
    for i in range(1, len(jolts)):
        d = jolts[i] - jolts[i - 1]
        if d == 1:
            ones += 1
        elif d == 3:
            threes += 1
    return ones, threes


def count_arrangements(jolts: List[int]) -> int:
    outlet = max(jolts) + 3
    jolts = jolts[:]
    jolts.append(0)
    jolts.append(outlet)

    def count(n: int, values: Set[int], cache: Dict[int, int]) -> int:
        if n in cache:
            return cache[n]
        if n == 0:
            cache[n] = 1
            return 1
        if n < 0:
            cache[n] = 0
            return 0
        if n not in values:
            cache[n] = 0
            return 0
        cache[n] = count(n - 1, values, cache) + count(n - 2, values, cache) + count(n - 3, values, cache)
        return cache[n]

    return count(outlet, set(jolts), {})


def part1(jolts: List[int]) -> None:
    ones, threes = find_distribution(jolts)
    print(ones * threes)


def part2(jolts: List[int]) -> None:
    print(count_arrangements(jolts))


class Test(unittest.TestCase):

    def test_find_distribution(self):
        data = [
            ([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4], (7, 5)),
            ([28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45,
              19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3], (22, 10))
        ]
        for jolts, dist in data:
            self.assertEqual(dist, find_distribution(jolts))

    def test_count_arrangements(self):
        data = [
            ([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4], 8),
            ([28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45,
              19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3], 19208)
        ]
        for jolts, cnt in data:
            self.assertEqual(cnt, count_arrangements(jolts))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            ints = [int(s) for s in infile.read().split('\n') if s]
            part1(ints)
            part2(ints)
    else:
        unittest.main()
