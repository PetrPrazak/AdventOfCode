# https://adventofcode.com/2021/day/17
from __future__ import print_function
from pathlib import Path
from math import sqrt
import re


def will_hit(velocity, target):
    pos = 0+0j
    minx, maxx = target[0]
    miny, maxy = target[1]
    on_target, highest = False, 0
    while not on_target:
        pos += velocity
        highest = max(highest, int(pos.imag))
        velocity = complex(max(velocity.real - 1, 0), velocity.imag - 1)
        on_target = pos.real in range(minx, maxx+1) and pos.imag in range(miny, maxy+1)
        if pos.real > maxx or pos.imag < miny:
            break
    return highest if on_target else None


def sim_probe(data):
    max_y, hits = 0, 0
    target_x, target_y = data
    for vel_x in range(round(sqrt(2 * target_x[0])), target_x[1]+1):
        for vel_y in range(target_y[0], abs(target_y[0])+1):
            highest = will_hit(complex(vel_x, vel_y), data)
            if highest is not None:
                hits += 1
                max_y = max(max_y, highest)
    return max_y, hits


def process(data):
    # part 1
    highest, all_velocities = sim_probe(data)
    print("part 1:", highest)
    # part 2
    print("part 2:", all_velocities)


def load_data(fileobj):
    tx1, tx2, ty1, ty2 = (map(int, re.findall("[-\d]+", fileobj.readline())))
    return (tx1, tx2), (ty1, ty2)


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
