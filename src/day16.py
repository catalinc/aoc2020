import re
import unittest
from collections import defaultdict
from typing import Dict, List, Tuple

import sys


class Rule:

    def __init__(self, name: str, ranges: List[List[int]]):
        self.name = name
        self.ranges = ranges

    def match(self, n: int) -> bool:
        for r in self.ranges:
            if r[0] <= n <= r[1]:
                return True

    def __str__(self):
        return f"{self.name}: {' '.join([str(r) for r in self.ranges])}"


def parse_rule(s: str) -> Rule:
    m = re.match(r"^([^:]+?):", s)
    name = m[1]
    ints = [int(x) for x in re.findall(r"\d+", s)]
    ranges = [ints[i:i + 2] for i in range(0, len(ints), 2)]
    return Rule(name=name, ranges=ranges)


def parse_input(s: str) -> Tuple[List[Rule], List[int], List[List[int]]]:
    s1, s2, s3 = re.split(r"(?m)^\s*$\s*", s)
    rules = [parse_rule(s) for s in s1.split('\n') if s]
    my = [int(s) for s in s2.split('\n')[1].split(',') if s]
    tickets = [[int(s) for s in line.split(',')] for line in s3.split('\n')[1:] if line]
    return rules, my, tickets


def scanning_error_rate(rules: List[Rule], tickets: List[List[int]]) -> int:
    rate = 0
    for t in tickets:
        for n in t:
            matched = False
            for r in rules:
                if r.match(n):
                    matched = True
                    break
            if not matched:
                rate += n
    return rate


def find_matching_rules(rules: List[Rule], ticket: List[int]) -> Dict[int, List[str]]:
    matches = defaultdict(list)
    for i, n in enumerate(ticket):
        for r in rules:
            if r.match(n):
                matches[i].append(r.name)
    return matches


def find_matching_fields(rules: List[Rule], tickets: List[List[int]]) -> Dict[str, int]:
    matches = {}
    for t in tickets:
        mr = find_matching_rules(rules, t)
        if len(mr) != len(rules):
            continue
        for i in range(len(t)):
            fs = matches.get(i)
            if not fs:
                matches[i] = set(mr[i])
            else:
                matches[i] = matches[i].intersection(mr[i])
    fields = {}
    while matches:
        matched = []
        for i, names in matches.items():
            if len(names) == 1:
                s = names.pop()
                fields[s] = i
                matched.append(s)
        for s in matched:
            for i, names in matches.items():
                if s in names:
                    names.remove(s)
        for s, i in fields.items():
            if i in matches:
                del matches[i]

    return fields


def part1(rules: List[Rule], tickets: List[List[int]]) -> None:
    print(scanning_error_rate(rules, tickets))


def part2(rules: List[Rule], my_ticket: List[int], tickets: List[List[int]]) -> None:
    fields = find_matching_fields(rules, tickets)
    p = 1
    for s, i in fields.items():
        if s.startswith("departure"):
            p *= my_ticket[i]
    print(p)


class Test(unittest.TestCase):

    def test_error_scanning_rate(self):
        s = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
        rs, _, ts = parse_input(s)
        self.assertEqual(71, scanning_error_rate(rs, ts))

    def test_find_matching_fields(self):
        s = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""
        rs, _, ts = parse_input(s)
        fs = find_matching_fields(rs, ts)
        self.assertEqual(0, fs["row"])
        self.assertEqual(1, fs["class"])
        self.assertEqual(2, fs["seat"])


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            rules_db, mine, others = parse_input(infile.read().rstrip())
            part1(rules_db, others)
            part2(rules_db, mine, others)
    else:
        unittest.main()
