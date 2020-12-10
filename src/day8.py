import unittest
from typing import Tuple, List

import sys


def run_program(instructions: List[str]) -> Tuple[bool, int]:
    pc, acc, hist = 0, 0, set()
    while pc < len(instructions):
        op, arg = decode(instructions[pc])
        if op == "nop":
            pc += 1
        elif op == "acc":
            acc += arg
            pc += 1
        elif op == "jmp":
            pc += arg
        if pc in hist:
            return False, acc
        hist.add(pc)
    return True, acc


def decode(instruction: str) -> Tuple[str, int]:
    op, arg = instruction.split(' ')
    return op, int(arg)


def break_loop(instructions: List[str]) -> int:
    for i, instr in enumerate(instructions):
        if instr.startswith('jmp'):
            new_instructions = instructions[:]
            new_instructions[i] = 'nop +0'
            done, acc = run_program(new_instructions)
            if done:
                return acc


def part1(instructions: List[str]) -> None:
    print(run_program(instructions))


def part2(instructions: List[str]) -> None:
    print(break_loop(instructions))


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.instructions = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""".split('\n')

    def test_decode(self):
        self.assertEqual(('jmp', -7), decode('jmp -7'))
        self.assertEqual(('nop', 0), decode('nop +0'))

    def test_run_program(self):
        self.assertEqual((False, 5), run_program(self.instructions))

    def test_break_loop(self):
        self.assertEqual(8, break_loop(self.instructions))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            lines = [l for l in infile.read().split('\n') if l]
            part1(lines)
            part2(lines)
    else:
        unittest.main()
