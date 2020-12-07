import re
import unittest
from collections import defaultdict, deque
from typing import Dict, Tuple, List

import sys


def parse_rules(s: str, color_to_parent) -> Dict[str, List[Tuple[str, int]]]:
    rules = defaultdict(list)
    for r in s.split('\n'):
        m = re.match(r'^(\w+ \w+)', r)
        if m:
            parent_color = m[0]
            for cnt, color in re.findall(r'(\d+) (\w+ \w+)', r):
                if color_to_parent:
                    rules[color].append((parent_color, int(cnt)))
                else:
                    rules[parent_color].append((color, int(cnt)))
    return rules


def part1(s: str) -> int:
    rules = parse_rules(s, color_to_parent=True)
    stack, visited, total = [], set(), 0
    for parent, _ in rules['shiny gold']:
        stack.append(parent)
    while stack:
        parent = stack.pop()
        if parent not in visited:
            visited.add(parent)
            total += 1
            for grand_parent, _ in rules[parent]:
                if grand_parent not in visited:
                    stack.append(grand_parent)
    return total


def part2(s: str) -> int:
    rules = parse_rules(s, color_to_parent=False)
    queue, total = deque([]), 0
    for child, count in rules['shiny gold']:
        queue.append((child, count))
    while queue:
        child, count = queue.popleft()
        total += count
        for grand_child, grand_child_count in rules[child]:
            queue.append((grand_child, count * grand_child_count))
    return total


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.input1 = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
        self.input2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

    def test_parse_rules(self):
        rs = parse_rules(self.input1, color_to_parent=True)
        self.assertEqual(7, len(rs))
        self.assertEqual([('light red', 2), ('dark orange', 4)], rs['muted yellow'])

    def test_part1(self):
        self.assertEqual(4, part1(self.input1))

    def test_part2(self):
        self.assertEqual(32, part2(self.input1))
        self.assertEqual(126, part2(self.input2))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            content = infile.read()
            print(part1(content))
            print(part2(content))
    else:
        unittest.main()
