# https://adventofcode.com/2015/day/21
from __future__ import print_function
from pathlib import Path
from collections import namedtuple
from itertools import product


START_HIT_POINTS = 100

Player = namedtuple('Player', 'hit_point damage armor')

Item = namedtuple('Item', 'name cost damage armor')
Weapons = [
    Item("Dagger", 8, 4, 0),
    Item("Shortsword", 10, 5, 0),
    Item("Warhammer", 25, 6, 0),
    Item("Longsword", 40, 7, 0),
    Item("Greataxe", 74, 8, 0)
]

Armor = [
    Item(None, 0, 0, 0),
    Item("Leather", 13, 0, 1),
    Item("Chainmail", 31, 0, 2),
    Item("Splintmail", 53, 0, 3),
    Item("Bandedmail", 75, 0, 4),
    Item("Platemail", 102, 0, 5)
]

Rings = [
    Item(None, 0, 0, 0),
    Item("Damage +1", 25, 1, 0),
    Item("Damage +2", 50, 2, 0),
    Item("Damage +3", 100, 3, 0),
    Item("Defense +1", 20, 0, 1),
    Item("Defense +2", 40, 0, 2),
    Item("Defense +3", 80, 0, 3)
]


def fight(player, boss):
    """ returns True if player wins """
    pl_damage = max(1, player.damage - boss.armor)
    boss_damage = max(1, boss.damage - player.armor)
    pl_round, pl_rem = divmod(player.hit_point, boss_damage)
    boss_round, boss_rem = divmod(boss.hit_point, pl_damage)
    return pl_round > boss_round \
        or pl_round == boss_round and pl_rem >= boss_rem


def process(data):
    boss = Player(data[0], data[1], data[2])
    min_cost, max_cost = 9999, 0
    for w, a, r1, r2 in product(Weapons, Armor, Rings, Rings):
        if r1.name and r2.name and r1 == r2:
            continue
        cost = w.cost + a.cost + r1.cost + r2.cost
        damage = w.damage + a.damage + r1.damage + r2.damage
        armor = w.armor + a.armor + r1.armor + r2.armor
        if fight(Player(START_HIT_POINTS, damage, armor), boss):
            min_cost = min(cost, min_cost)
        else:
            max_cost = max(cost, max_cost)

    # part 1
    print("part 1:", min_cost)
    # part 2
    print("part 2:", max_cost)


def parse_line(line):
    return int(line.strip().split(': ')[1])


def load_data(fileobj):
    return [parse_line(line) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
