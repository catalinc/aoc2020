import sys
import unittest

from typing import List, Tuple


class Math:
    LEFT_ASSOC = 0
    RIGHT_ASSOC = 1

    def __init__(self):
        self.ops = {'+': (0, Math.LEFT_ASSOC),
                    '*': (0, Math.LEFT_ASSOC)}

    def is_op(self, c: str) -> bool:
        return c in self.ops

    def cmp_prec(self, op1: str, op2: str) -> int:
        return self.ops[op1][0] - self.ops[op2][0]

    def set_op(self, op: str, spec: Tuple[int, int]):
        self.ops[op] = spec

    def is_left_assoc(self, op: str) -> bool:
        return self.ops[op][1] == Math.LEFT_ASSOC


def eval_expr(e: str, math: Math = None) -> int:
    if not math:
        math = Math()
    e = to_rpn(e, math)
    return eval_rpn(e)


def to_rpn(e: str, math: Math = None) -> str:
    if not math:
        math = Math()
    out, op_stack = [], []
    for x in e:
        if x == ' ':
            continue
        if math.is_op(x):
            if op_stack:
                while op_stack and math.is_op(op_stack[-1]) and \
                        (math.cmp_prec(x, op_stack[-1]) < 0 or
                         (math.cmp_prec(x, op_stack[-1]) == 0 and math.is_left_assoc(x))):
                    out.append(op_stack.pop())
            op_stack.append(x)
        elif x == '(':
            op_stack.append(x)
        elif x == ')':
            while op_stack and op_stack[-1] != '(':
                out.append(op_stack.pop())
            if op_stack and op_stack[-1] == '(':
                op_stack.pop()
        else:
            out.append(x)
    while op_stack:
        out.append(op_stack.pop())
    return ' '.join(out)


def eval_rpn(e: str) -> int:
    stack = []
    for x in e:
        if x == ' ':
            continue
        if x == '+':
            n1 = stack.pop()
            n2 = stack.pop()
            stack.append(n1 + n2)
        elif x == '*':
            n1 = stack.pop()
            n2 = stack.pop()
            stack.append(n1 * n2)
        else:
            stack.append(int(x))
    return stack[0]


def part1(exprs: List[str]) -> None:
    t = 0
    for e in exprs:
        t += eval_expr(e)
    print(t)


def part2(exprs: List[str]) -> None:
    math = Math()
    math.set_op('+', (1, Math.LEFT_ASSOC))
    t = 0
    for e in exprs:
        t += eval_expr(e, math)
    print(t)


class Test(unittest.TestCase):

    def test_to_rpn(self):
        self.assertEqual('1 2 + 3 +', to_rpn('1 + 2 + 3'))
        self.assertEqual('1 2 3 * +', to_rpn('1 + (2 * 3)'))
        self.assertEqual('1 2 3 * + 4 5 6 + * +', to_rpn('1 + (2 * 3) + (4 * (5 + 6))'))
        self.assertEqual('5 8 3 * 9 + 3 + 4 * 3 * +', to_rpn('5 + (8 * 3 + 9 + 3 * 4 * 3)'))

    def test_eval_expr(self):
        test_data = [
            ('1 + 2 * 3 + 4 * 5 + 6', 71),
            ('1 + (2 * 3) + (4 * (5 + 6))', 51),
            ('2 * 3 + (4 * 5)', 26),
            ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 437),
            ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 12240),
            ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632)
        ]
        for e, n in test_data:
            self.assertEqual(n, eval_expr(e), f"failed for: {e}")

    def test_eval_expr_add_before_mul(self):
        test_data = [
            ('1 + 2 * 3 + 4 * 5 + 6', 231),
            ('1 + (2 * 3) + (4 * (5 + 6))', 51),
            ('2 * 3 + (4 * 5)', 46),
            ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 1445),
            ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 669060),
            ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 23340)
        ]
        math = Math()
        math.set_op('+', (1, Math.LEFT_ASSOC))
        for e, n in test_data:
            self.assertEqual(n, eval_expr(e, math), f"failed for: {e}")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            lines = [s for s in infile.read().split('\n') if s]
            part1(lines)
            part2(lines)
    else:
        unittest.main()
