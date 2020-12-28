import sys
import unittest


def part1(card_pk: int, door_pk: int) -> int:
    loop = find_loop_size(7, card_pk)
    return transform(door_pk, loop)


def transform(subject: int, loop_size: int, n: int = 1) -> int:
    while loop_size > 0:
        n *= subject
        n %= 20201227
        loop_size -= 1
    return n


def find_loop_size(subject: int, public_key: int, size: int = 1) -> int:
    n = transform(subject, size)
    while True:
        if n == public_key:
            return size
        n = transform(subject, 1, n)
        size += 1


def part2():
    pass


class Test(unittest.TestCase):

    def test_find_loop_size(self):
        self.assertEqual(8, find_loop_size(7, 5764801))
        self.assertEqual(11, find_loop_size(7, 17807724))

    def test_part1(self):
        self.assertEqual(14897079, part1(17807724, 5764801))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            pk1 = int(infile.readline())
            pk2 = int(infile.readline())
            print(part1(pk1, pk2))
            part2()
    else:
        unittest.main()
