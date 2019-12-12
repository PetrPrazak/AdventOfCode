# https://adventofcode.com/2019/day/12
from __future__ import print_function
from itertools import combinations
from math import gcd
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from aoc import *

INPUT = "aoc2019_12_input.txt"
TEST = "test.txt"
TEST2 = "test2.txt"


# the moon is represented as a list with 6 numbers:
# positions and velocities in each plane
def get_body(position):
    body = position
    body.extend([0] * 3)
    return body


def compare_axis(axis1, axis2):
    return 0 if axis1 == axis2 else 1 if axis1 < axis2 else -1


def apply_gravity(moon1, moon2):
    for i in range(3):
        cmp = compare_axis(moon1[i], moon2[i])
        moon1[i + 3] += cmp
        moon2[i + 3] -= cmp


def move(m):
    for i in range(3):
        m[i] += m[i + 3]


def potential_energy(moon):
    return sum([abs(c) for c in moon[:3]])


def kinetic_energy(moon):
    return sum([abs(c) for c in moon[3:]])


def energy(moon):
    return potential_energy(moon) * kinetic_energy(moon)


def parse_coord(line):
    return [int(c.split('=')[1]) for c in line.replace(">", "").split(",")]


def timestep(moons):
    for m1, m2 in combinations(range(len(moons)), 2):
        apply_gravity(moons[m1], moons[m2])
    for m in moons:
        move(m)


# the least common multiple
def lcm(x, y):
    return x * y // gcd(x, y)


def cut_plane(moons, plane):
    return [(m[plane], m[plane + 3]) for m in moons]


@timeit
def process(data, steps):
    # part 1
    moons = [get_body(parse_coord(l)) for l in data]
    for s in range(steps):
        timestep(moons)
    total_energy = sum([energy(m) for m in moons])
    print("Energy sum after %d steps:" % steps, total_energy)  # 7179

    # part 2
    # the trick is to search for repetitions separately for each place
    # then the result is the least common multiple of all steps
    # it would be faster not to count all planes in each step, but whatever...
    moons = [get_body(parse_coord(l)) for l in data]
    steps = [0] * 3
    for i in range(3):
        orig_state = cut_plane(moons, i)
        new_state = None
        step = 0
        while new_state != orig_state:
            timestep(moons)
            step += 1
            new_state = cut_plane(moons, i)
        steps[i] = step
    total = lcm(lcm(steps[0], steps[1]), steps[2])
    print("Total steps needed:", total)  # 428576638953552


def test():
    data = read_input_lines(TEST)
    process(data, 10)


def test2():
    data = read_input_lines(TEST2)
    process(data, 100)


def main():
    data = read_input_lines(INPUT)
    process(data, 1000)


if __name__ == "__main__":
    # test()
    # test2()
    main()
