# https://adventofcode.com/2024/day/8
from pathlib import Path
from collections import defaultdict
from itertools import combinations
import time


def count_nodes(antennas, height, width, part=1):
    def in_range(pos):
        return pos.real in range(height) and pos.imag in range(width)
    antinodes = set()
    for positions in antennas.values():
        for a1, a2 in combinations(positions, 2):
            da = a1 - a2
            for node, step in ((a1, da), (a2, -da)):
                if part == 2:
                    antinodes.add(node)
                antinode = node + step
                while in_range(antinode):
                    antinodes.add(antinode)
                    if part == 1:
                        break
                    antinode += step
    return len(antinodes)


def process(data):
    height, width = len(data), len(data[0])
    antennas = defaultdict(list)
    for r, row in enumerate(data):
        for c, a in enumerate(row):
            if a != '.':
                antennas[a].append(complex(r, c))

    # part 1
    result = count_nodes(antennas, height, width)
    print("part 1:", result)

    # part 2
    result = count_nodes(antennas, height, width, part=2)
    print("part 2:", result)


def load_data(fileobj):
    return [line.rstrip() for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    # main("test.txt")
    main()
