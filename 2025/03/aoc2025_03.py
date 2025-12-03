# https://adventofcode.com/2025/day/3
from pathlib import Path
import time


def max_num(line):
    x, pos = None, -1
    for i, n in enumerate(line):
        if not x or n > x:
            x = n
            pos = i
    return x, pos


def max_joltage(line, size=2):
    jolt = ""
    spos = 0
    for l in range(1, size + 1):
        x, px = max_num(line[spos:len(line)-size+l])
        jolt += x
        spos += px + 1
    return int(jolt)


def part1(data):
    return sum(max_joltage(l) for l in data)


def part2(data):
    return sum(max_joltage(l, size=12) for l in data)


def process(data):
    # part 1
    result = part1(data)
    print("part 1:", result)
    # part 2
    result = part2(data)
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
