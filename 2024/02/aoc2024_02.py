# https://adventofcode.com/2024/day/2
from pathlib import Path
import time


def is_good(l):
    difs = all(0 < abs(a-b) <= 3 for a, b in zip(l, l[1:]))
    signs = all(a < b for a, b in zip(l, l[1:])) or all(a > b for a, b in zip(l, l[1:]))
    return difs and signs


def one_less(l):
    for i in range(0, len(l)):
        yield l[0:i] + l[i+1:]


def is_good2(l):
    return any(is_good(ll) for ll in one_less(l))


def process(data):
    part1 = part2 = 0
    for l in data:
        part1 += is_good(l)
        part2 += is_good2(l)
    # part 1
    print("part 1:", part1)
    # part 2
    print("part 2:", part2)


def parse_line(line):
    return [int(n) for n in line.split()]


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj.readlines()]
  

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
