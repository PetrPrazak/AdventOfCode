# https://adventofcode.com/2019/day/06

from __future__ import print_function

INPUT = "aoc2019_06_input.txt"


def get_depth(orbits, orbit):
    if not orbits[orbit]:
        return 0
    return 1 + get_depth(orbits, orbits[orbit])


def get_path(orbits, orbit, parents):
    parent = orbits[orbit]
    if not parent:
        return []
    parents.append(parent)
    get_path(orbits, orbits[orbit], parents)
    return parents


def process(data):
    # part 1
    orbits = {o[1]: o[0] for o in data}
    orbits["COM"] = None
    depths = [get_depth(orbits, o) for o in orbits.keys()]
    print(sum(depths))

    # part 2
    you = get_path(orbits, "YOU", [])
    san = get_path(orbits, "SAN", [])

    for p in you:
        if p in san:
            break

    print(you.index(p) + san.index(p))


def main():
    with open(INPUT) as f:
        data = [l.strip().split(")") for l in f.readlines()]
        process(data)


if __name__ == "__main__":
    main()
