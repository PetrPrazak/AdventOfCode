# https://adventofcode.com/2025/day/5
from pathlib import Path
import time


def check_id(ranges, id):
    for s, e in ranges:
        if id in range(s, e+1):
            return True
    return False


def part1(ranges, ids):
    return sum(check_id(ranges, id) for id in ids)


def part2(ranges):
    acc = 0
    end_max = 0
    for start, end in sorted(ranges):
        if end >= end_max:
            acc += end - max(start, end_max) + 1
            end_max = end + 1
    return acc


def process(data):
    # part 1
    ranges, ids = data
    result = part1(ranges, ids)
    print("part 1:", result)
    # part 2
    result = part2(ranges)
    print("part 2:", result)


def parse_line(line):
    start, end = line.split('-')
    return int(start), int(end)


def load_data(fileobj):
    ranges, ids = fileobj.read().split("\n\n")
    return [parse_line(line.rstrip()) for line in ranges.split('\n')], [int(id) for id in ids.split('\n')]


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
