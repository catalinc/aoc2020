import re
import unittest
from typing import Generator, Any

import sys


class MaskV1:
    def __init__(self, spec):
        self.mset = int(spec.replace('X', '0'), 2)
        self.mclr = int(spec.replace('X', '1'), 2)

    def apply(self, n: int) -> int:
        n = n | self.mset
        n = n & self.mclr
        return n


def run_program_v1(s: str) -> int:
    lines = [line for line in s.split('\n') if s]
    mem = {}
    mask = None
    for line in lines:
        m = re.match("mask = ([X01]+)", line)
        if m:
            mask = MaskV1(m[1])
        else:
            m = re.match("mem\\[(\\d+)] = (\\d+)", line)
            if m:
                addr, val = int(m[1]), int(m[2])
                val = mask.apply(val)
                mem[addr] = val
    return sum(mem.values())


def part1(s: str) -> None:
    print(run_program_v1(s))


def run_program_v2(s: str) -> int:
    lines = [line for line in s.split('\n') if s]
    mem = {}
    mask = None
    for line in lines:
        m = re.match("mask = ([X01]+)", line)
        if m:
            mask = m[1]
        else:
            m = re.match("mem\\[(\\d+)] = (\\d+)", line)
            if m:
                addr, val = int(m[1]), int(m[2])
                for n in mask_v2(mask, addr):
                    mem[n] = val
    return sum(mem.values())


def mask_v2(m: str, n: int) -> Generator[int, Any, None]:
    nm = bin(n)[2:].rjust(36, '0')
    bits = []
    for i in range(len(m)):
        dm = m[i]
        dn = nm[i]
        if dm == 'X':
            bits.append(dm)
        elif dm == '0':
            bits.append(dn)
        elif dm == '1':
            bits.append('1')
    s = ''.join(bits)
    return gen(s)


def gen(s, i=0):
    if i >= len(s):
        yield int(s, 2)
    else:
        while i < len(s) and s[i] != 'X':
            i += 1
        if i >= len(s):
            yield int(s, 2)
        else:
            yield from gen(s[:i] + '0' + s[i + 1:], i + 1)
            yield from gen(s[:i] + '1' + s[i + 1:], i + 1)


def part2(s: str) -> None:
    print(run_program_v2(s))


class Test(unittest.TestCase):

    def test_mask_v1(self):
        m = MaskV1('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X')
        self.assertEqual(73, m.apply(11))
        self.assertEqual(101, m.apply(101))
        self.assertEqual(64, m.apply(0))

    def test_run_program_v1(self):
        prg = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""
        self.assertEqual(165, run_program_v1(prg))

    def test_mask_v2(self):
        m = "000000000000000000000000000000X1001X"
        self.assertEqual([26, 27, 58, 59], list(mask_v2(m, 42)))
        m = '00000000000000000000000000000000X0XX'
        self.assertEqual([16, 17, 18, 19, 24, 25, 26, 27], list(mask_v2(m, 26)))

    def test_run_program_v2(self):
        prg = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""
        self.assertEqual(208, run_program_v2(prg))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            prog = infile.read()
            part1(prog)
            part2(prog)
    else:
        unittest.main()
