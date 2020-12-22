import sys
import re
import unittest

from collections import Counter
from operator import itemgetter


def parse_food(line: str) -> tuple[list[str], list[str]]:
    ingredients = []
    allergens = []
    collect = ingredients
    for name in re.findall(r'\w+', line):
        if name == 'contains':
            collect = allergens
            continue
        collect.append(name)
    return allergens, ingredients


def part1(lines: list[str]) -> tuple[int, dict[str, set[str]]]:
    bad_foods = {}
    all_ingredients = set()
    ingredients_counter = Counter()
    for line in lines:
        allergens, ingredients = parse_food(line)
        mapping = {}
        for name in allergens:
            mapping[name] = set(ingredients)
        for name in allergens:
            if name in bad_foods:
                bad_foods[name] &= mapping[name]
            else:
                bad_foods[name] = mapping[name]
        all_ingredients.update(ingredients)
        ingredients_counter.update(ingredients)
    bad_ingredients = set()
    for ingredients in bad_foods.values():
        bad_ingredients.update(ingredients)
    safe_ingredients = all_ingredients - bad_ingredients
    count = 0
    for name in safe_ingredients:
        count += ingredients_counter[name]
    return count, bad_foods


def part2(bad_foods: dict[str, set[str]]) -> str:
    dangerous = []
    while bad_foods:
        to_del = []
        for allergen, ingredients in bad_foods.items():
            if len(ingredients) == 1:
                name = ingredients.pop()
                dangerous.append((name, allergen))
                to_del.append((allergen, name))
        for allergen, ingredient in to_del:
            bad_foods.pop(allergen)
            for ingredients in bad_foods.values():
                if ingredient in ingredients:
                    ingredients.remove(ingredient)
    dangerous.sort(key=itemgetter(1))
    return ','.join([t[0] for t in dangerous])


class Test(unittest.TestCase):

    def setUp(self) -> None:
        s = """
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""
        self.lines = [line for line in s.split('\n') if line]

    def test_part1(self):
        self.assertEqual(5, part1(self.lines)[0])

    def test_part2(self):
        bad_foods = part1(self.lines)[1]
        self.assertEqual('mxmxvkd,sqjhc,fvjkl', part2(bad_foods))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as infile:
            inputs = [line for line in infile.read().split('\n') if line]
            total, dangerous_foods = part1(inputs)
            print(total)
            print(part2(dangerous_foods))
    else:
        unittest.main()
