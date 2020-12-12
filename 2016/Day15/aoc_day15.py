# http://adventofcode.com/2016/day/15
from __future__ import print_function
import re


def get_pos(time, disk, positions, at):
    return (time + disk + at) % positions


def brute_force(data):
    for t in range(1, 10000000):
        if all(get_pos(t, disk, pos, at) == 0 for disk, pos, at in data):
            return t
    return None


def solve(data):
    # part 1
    result = brute_force(data)
    print("Part 1:", result)
    # part 2
    data.append((len(data)+1, 11, 0))
    result = brute_force(data)
    print("Part 2:", result)


def parse(line):
    disk, pos, _, at = re.findall(r'\d+', line)
    return int(disk), int(pos), int(at)


def main(file):
    print(file)
    with open(file) as f:
        lines = [parse(l.strip()) for l in f.readlines()]
        solve(lines)


if __name__ == "__main__":
    # main("test.txt")
    main("input.txt")
