import re
import sys
import unittest
from collections import namedtuple
from typing import Tuple

Rule = namedtuple("Rule", ["id", "type", "sub_rules"])


class RuleDb:
    RTYPE1 = 1
    RTYPE2 = 2
    RTYPE3 = 3

    def __init__(self, s: str):
        self.db = {}
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
        matched, pos = self.match_at_pos(rule_id, 0, s)
        return matched and pos == len(s)

    def match_at_pos(self, rule_id: int, start: int, s: str) -> Tuple[bool, int]:
        if start >= len(s):
            return False, start
        pos = start
        rule = self.db[rule_id]
        sub_rules = rule.sub_rules
        if rule.type == RuleDb.RTYPE1:
            sub_rules_left = sub_rules[0]
            matched = True
            for i in sub_rules_left:
                matched, pos = self.match_at_pos(i, pos, s)
                if not matched:
                    break
            if not matched:
                pos = start
                sub_rules_right = sub_rules[1]
                for i in sub_rules_right:
                    matched, pos = self.match_at_pos(i, pos, s)
                    if not matched:
                        break
            return matched, pos
        elif rule.type == RuleDb.RTYPE2:
            return rule.sub_rules[0] == s[pos], pos + 1
        elif rule.type == RuleDb.RTYPE3:
            matched = True
            for i in sub_rules:
                matched, pos = self.match_at_pos(i, pos, s)
                if not matched:
                    break
            return matched, pos


def part1(s: str) -> None:
    sections = tuple(x for x in re.split(r"(?m)^\s*$\s*", s) if x)
    rspec, msgs = sections
    rdb = RuleDb(rspec)
    cnt = 0
    for m in msgs.split('\n'):
        if m and rdb.match(0, m):
            cnt += 1
    print(cnt)


def part2() -> None:
    pass


class Test(unittest.TestCase):

    def test_rule_db_match(self):
        rdb = RuleDb("""
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
            self.assertEqual(t, rdb.match(0, s), f"failed for {s}")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            part1(infile.read())
    else:
        unittest.main()
