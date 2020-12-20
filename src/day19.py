import re
import sys
import unittest
from collections import namedtuple
from typing import Tuple, List

Rule = namedtuple("Rule", ["id", "type", "sub_rules"])


class RuleDb:
    RTYPE1 = 1
    RTYPE2 = 2
    RTYPE3 = 3

    def __init__(self, s: str):
        self.db = {}
        self.pre = {}
        lines = [s for s in s.split('\n') if s]
        for line in lines:
            rule = self.parse_rule(line)
            self.db[rule.id] = rule

    @staticmethod
    def parse_rule(s: str) -> Rule:
        head, tail = s.split(': ')
        rule_id = int(head)
        sub_rules, rule_type = [], -1
        if '|' in tail:
            rule_type = RuleDb.RTYPE1
            left, right = tail.split(' | ')
            left = [int(x) for x in left.split(' ')]
            right = [int(x) for x in right.split(' ')]
            sub_rules.append(left)
            sub_rules.append(right)
        elif '"' in tail:
            rule_type = RuleDb.RTYPE2
            pos = tail.index('"')
            ch = tail[pos + 1: pos + 2]
            sub_rules.append(ch)
        else:
            rule_type = RuleDb.RTYPE3
            sub_rules = [int(x) for x in tail.split(' ')]
        return Rule(rule_id, rule_type, sub_rules)

    def match(self, rule_id: int, s: str) -> bool:
        pattern = "^" + self.to_regex(rule_id) + "$"
        return bool(re.match(pattern, s))

    def to_regex(self, rule_id: 0) -> str:
        if rule_id in self.pre:
            return self.pre[rule_id]
        rule = self.db[rule_id]
        sub_rules = rule.sub_rules
        if rule.type == RuleDb.RTYPE1:
            left = ''
            for rid in sub_rules[0]:
                left += self.to_regex(rid)
            right = ''
            for rid in sub_rules[1]:
                right += self.to_regex(rid)
            return '(' + left + '|' + right + ')'
        elif rule.type == RuleDb.RTYPE2:
            return sub_rules[0]
        elif rule.type == RuleDb.RTYPE3:
            pattern = '('
            for rid in sub_rules:
                pattern += self.to_regex(rid)
            return pattern + ')'

    def set_rule(self, rule_id: int, pattern: str):
        self.pre[rule_id] = pattern


def parse_input(s: str) -> Tuple[RuleDb, List[str]]:
    sections = tuple(x for x in re.split(r"(?m)^\s*$\s*", s) if x)
    rule_db = RuleDb(sections[0])
    messages = [m for m in sections[1].split('\n') if m]
    return rule_db, messages


def part1(rule_db: RuleDb, messages: List[str]) -> None:
    cnt = 0
    for m in messages:
        if rule_db.match(0, m):
            cnt += 1
    print(cnt)


def part2(rule_db: RuleDb, messages: List[str]) -> None:
    r42 = rule_db.to_regex(42)
    r31 = rule_db.to_regex(31)
    rule_db.set_rule(8, f"{r42}+")
    matches, i = set(), 2
    while i <= 10:
        rule_db.set_rule(11, f"({r42}{r31}|{r42}{{{i}}}{r31}{{{i}}})")
        for m in messages:
            if rule_db.match(0, m):
                matches.add(m)
        i += 1
    print(len(matches))


class Test(unittest.TestCase):

    def test_rule_db_match(self):
        rule_db = RuleDb("""
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
""")
        test_data = [(True, 'ababbb'), (True, 'abbbab'),
                     (False, 'bababa'), (False, 'aaabbb'), (False, 'aaaabbb')]
        for t, s in test_data:
            self.assertEqual(t, rule_db.match(0, s), f"failed for {s}")

    def test_rule_db_match_with_updated_rules(self):
        rule_db = RuleDb("""
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1
""")

        messages = """
abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""
        matches = []
        for m in messages.split('\n'):
            if m and rule_db.match(0, m):
                matches.append(m)

        self.assertEqual(3, len(matches))

        r42 = rule_db.to_regex(42)
        r31 = rule_db.to_regex(31)
        rule_db.set_rule(8, f"{r42}+")
        i = 2
        matches = set()
        while i <= 10:
            rule_db.set_rule(11, f"({r42}{r31}|{r42}{{{i}}}{r31}{{{i}}})")
            for m in messages.split('\n'):
                if m and rule_db.match(0, m):
                    matches.add(m)
            i += 1

        self.assertEqual(12, len(matches))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            rdb, msgs = parse_input(infile.read())
            part1(rdb, msgs)
            part2(rdb, msgs)
    else:
        unittest.main()
