import sys
import unittest


def crab_game_small(cups: str, rounds: int) -> str:
    cl = CircularList()
    for n in (int(ch) for ch in cups):
        cl.add(n)
    while rounds > 0:
        picks = cl.after(cl.head, 3)
        for n in picks:
            cl.remove(n)
        dest = cl.head - 1
        while dest not in cl:
            if dest < cl.min_item:
                dest = cl.max_item
                break
            dest -= 1
        start = dest
        for n in picks:
            cl.insert(start, n)
            start = n
        cl.move_head()
        rounds -= 1
    cups = cl.after(1, len(cups) - 1)
    return ''.join(str(n) for n in cups)


def crab_game_big(cups: str, rounds: int, max_val: int) -> int:
    cl = CircularList()
    for n in (int(ch) for ch in cups):
        cl.add(n)
    for n in range(cl.max_item + 1, max_val + 1):
        cl.add(n)
    while rounds > 0:
        picks = cl.after(cl.head, 3)
        for n in picks:
            cl.remove(n)
        dest = cl.head - 1
        while dest not in cl:
            if dest < cl.min_item:
                dest = cl.max_item
                break
            dest -= 1
        start = dest
        for n in picks:
            cl.insert(start, n)
            start = n
        cl.move_head()
        rounds -= 1
    cups = cl.after(1, 2)
    return cups[0] * cups[1]


class Link:

    def __init__(self, pre: int = -1, nxt: int = -1):
        self.pre = pre
        self.nxt = nxt


class CircularList:

    def __init__(self):
        self.nodes = {}
        self.head = None
        self.tail = None
        self.min_item = sys.maxsize
        self.max_item = -sys.maxsize

    def add(self, item: int):
        if not self.head:
            self.head = item
            self.tail = item
            self.nodes[item] = Link()
        else:
            self.nodes[item] = Link(pre=self.tail, nxt=self.head)
            self.nodes[self.tail].nxt = item
            self.tail = item
            self.nodes[self.head].pre = item
        self.min_item = min(item, self.min_item)
        self.max_item = max(item, self.max_item)

    def remove(self, item: int):
        crt = self.nodes[item]
        nxt = self.nodes[crt.nxt]
        pre = self.nodes[crt.pre]
        nxt.pre = crt.pre
        pre.nxt = crt.nxt
        del self.nodes[item]
        if item == self.head:
            self.head = crt.nxt
        if item == self.tail:
            self.tail = crt.nxt
        if item == self.min_item:
            self.min_item = min(self.nodes.keys())
        if item == self.max_item:
            self.max_item = max(self.nodes.keys())

    def after(self, start: int, how_many: int) -> list[int]:
        result = []
        for i in range(how_many):
            start = self.nodes[start].nxt
            result.append(start)
        return result

    def insert(self, start: int, item: int):
        self.nodes[item] = Link()
        new = self.nodes[item]
        crt = self.nodes[start]
        nxt = self.nodes[crt.nxt]
        new.nxt = crt.nxt
        new.pre = start
        crt.nxt = item
        nxt.pre = item
        self.min_item = min(item, self.min_item)
        self.max_item = max(item, self.max_item)

    def move_head(self):
        self.head = self.nodes[self.head].nxt

    def __contains__(self, item):
        return item in self.nodes


def part1() -> None:
    print(crab_game_small('156794823', 100))


def part2() -> None:
    print(crab_game_big('156794823', 10_000_000, 1_000_000))


class Test(unittest.TestCase):

    def test_crab_game_small(self):
        self.assertEqual('92658374', crab_game_small('389125467', 10))
        self.assertEqual('67384529', crab_game_small('389125467', 100))

    def test_crab_game_big(self):
        self.assertEqual(149245887792, crab_game_big('389125467', 10_000_000, 1_000_000))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        part1()
        part2()
    else:
        unittest.main()
