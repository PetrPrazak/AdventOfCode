# https://adventofcode.com/2021/day/6
from __future__ import print_function
from pprint import pprint
from pathlib import Path
from copy import copy


def explode_fish(fish, cnt):
    """ stupid brute-force method """
    fish = fish.copy()
    for y in range(cnt):
        f_len = len(fish)
        for i in range(f_len):
            f = fish[i]
            newf = f-1 if f > 0 else 6
            fish[i] = newf
            if f == 0:
                fish.append(8)
    return len(fish)


def count_fish(fish, cnt):
    """ just count fishes of each iteration separately """
    growth = [0] * 9  # each fish can have iteration from 0 to 8
    for f in fish:
        growth[f] += 1

    for r in range(cnt):
        spawn = growth[0]  # how many are spawning in this iteration
        # shift generation, add newborn with iteration 8
        growth = growth[1:] + [spawn]
        growth[6] += spawn  # the spawning fish go to 6 again
    return sum(growth)


def process(data):
    # part 1
    fish = list(data)
    result = explode_fish(fish, 80)
    print("part 1:", result)
    # part 2
    result = count_fish(fish, 256)
    print("part 2:", result)


def load_data(fileobj):
    return map(int, fileobj.readline().rstrip().split(','))


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
