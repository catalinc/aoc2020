import re
import unittest
from typing import Dict, List

import sys

FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}


def parse_passports(s: str) -> List[Dict[str, str]]:
    res = []
    for p in re.split(r"(?m)^\s*$\s*", s):
        res.append(dict(re.findall(r"(\w+):([a-zA-Z0-9#]+)", p)))
    return res


def has_req_fields(passport: Dict[str, str]) -> bool:
    diff = FIELDS - set(passport.keys())
    return (not diff) or (diff == {'cid'})


def has_valid_fields(passport: Dict[str, str]):
    if not is_int_in_range(passport.get('byr'), 4, 1920, 2002):
        return False
    if not is_int_in_range(passport.get('iyr'), 4, 2010, 2020):
        return False
    if not is_int_in_range(passport.get('eyr'), 4, 2020, 2030):
        return False
    if not is_valid_hgt(passport.get('hgt')):
        return False
    if not is_valid_hcl(passport.get('hcl')):
        return False
    if not is_valid_ecl(passport.get('ecl')):
        return False
    if not is_valid_pid(passport.get('pid')):
        return False
    return True


def is_int_in_range(s: str, length: int, min_val: int, max_val: int) -> bool:
    if not s:
        return False
    p = "^\\d{" + str(length) + "}$"
    m = re.match(p, s)
    if m:
        n = int(m.group())
        return min_val <= n <= max_val
    return False


def is_valid_hgt(s: str) -> bool:
    if not s:
        return False
    m = re.match("^(\\d{2,3})(in|cm)$", s)
    if m:
        h = int(m.group(1))
        u = m.group(2)
        if u == "in":
            return 59 <= h <= 76
        if u == "cm":
            return 150 <= h <= 193
    return False


def is_valid_hcl(s: str) -> bool:
    if not s:
        return False
    m = re.match("^#[0-9a-f]{6}$", s)
    return bool(m)


def is_valid_pid(s: str) -> bool:
    if not s:
        return False
    return bool(re.match("^\\d{9}$", s))


def is_valid_ecl(s: str) -> bool:
    return s in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def part1(passports: List[Dict[str, str]]) -> None:
    cnt = 0
    for p in passports:
        if has_req_fields(p):
            cnt += 1
    print(cnt)


def part2(passports: List[Dict[str, str]]) -> None:
    cnt = 0
    for p in passports:
        if has_valid_fields(p):
            cnt += 1
    print(cnt)


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.input = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
        byr:1937 iyr:2017 cid:147 hgt:183cm
        
        iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
        hcl:#cfa07d byr:1929
        
        hcl:#ae17e1 iyr:2013
        eyr:2024
        ecl:brn pid:760753108 byr:1931
        hgt:179cm
        
        hcl:#cfa07d eyr:2025 pid:166559648
        iyr:2011 ecl:brn hgt:59in"""

    def test_parse_passports(self):
        passports = parse_passports(self.input)
        self.assertEqual(4, len(passports))
        first = passports[0]
        self.assertEqual('gry', first['ecl'])
        self.assertEqual('860033327', first['pid'])
        self.assertEqual('2020', first['eyr'])
        self.assertEqual('#fffffd', first['hcl'])
        self.assertEqual('1937', first['byr'])
        self.assertEqual('147', first['cid'])
        self.assertEqual('183cm', first['hgt'])

    def test_has_req_fields(self):
        passports = parse_passports(self.input)
        for i, v in [(0, True), (1, False), (2, True), (3, False)]:
            p = passports[i]
            self.assertEqual(v, has_req_fields(p), f"failed for {p}")

    def test_is_int_in_range(self):
        self.assertTrue(is_int_in_range('2002', 4, 1920, 2002))
        self.assertFalse(is_int_in_range('2003', 4, 1920, 2002))
        self.assertFalse(is_int_in_range('', 2, 12, 99))

    def test_is_valid_hgt(self):
        self.assertTrue(is_valid_hgt('60in'))
        self.assertTrue(is_valid_hgt('190cm'))
        self.assertFalse(is_valid_hgt('190in'))
        self.assertFalse(is_valid_hgt('190'))
        self.assertFalse(is_valid_hgt(''))

    def test_is_valid_hcl(self):
        self.assertTrue(is_valid_hcl('#123abc'))
        self.assertFalse(is_valid_hcl('#123abz'))
        self.assertFalse(is_valid_hcl('123abc'))
        self.assertFalse(is_valid_hcl(''))

    def test_is_valid_ecl(self):
        self.assertTrue(is_valid_ecl('brn'))
        self.assertFalse(is_valid_ecl('wat'))
        self.assertFalse(is_valid_ecl(''))

    def test_is_valid_pid(self):
        self.assertTrue(is_valid_pid('000000001'))
        self.assertFalse(is_valid_pid('0123456789'))
        self.assertFalse(is_valid_pid(''))

    def test_has_valid_fields(self):
        invalid = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""
        passports = parse_passports(invalid)
        for p in passports:
            self.assertFalse(has_valid_fields(p), f'failed for {p}')

        valid = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""
        passports = parse_passports(valid)
        for p in passports:
            self.assertTrue(has_valid_fields(p), f'failed for {p}')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            entries = parse_passports(infile.read())
            part1(entries)
            part2(entries)
    else:
        unittest.main()
