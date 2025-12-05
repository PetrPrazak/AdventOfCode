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
    def sum_range(s, e): return e - s + 1
    acc = 0
    p_s, p_e = None, None
    for s, e in sorted(ranges):
        if p_s is None:
            p_s, p_e = s, e
            continue
        if s > p_e:
            # non-overlapping range
            acc += sum_range(p_s, p_e)
            p_s, p_e = s, e
        else:
            if e > p_e:
                # overlapping partially
                acc += sum_range(p_s, s)
                p_s, p_e = s + 1, e
            else:
                # overlapping totally, can be ignored
                pass
    # last segment
    if p_s is not None:
        acc += sum_range(p_s, p_e)
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
