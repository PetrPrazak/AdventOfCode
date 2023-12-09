# https://adventofcode.com/2023/day/9
from pathlib import Path
import time


def diff_seq(intlist):
    return [b - a for a, b in zip(intlist, intlist[1:])]


def solve(history):
    diffs = []
    d = diff_seq(history)
    while any(d):
        diffs.append(d)
        d = diff_seq(d)

    next_seq, prev_seq = 0, 0
    for d in reversed(diffs):
        next_seq += d[-1]
        prev_seq = d[0] - prev_seq

    return history[-1] + next_seq, history[0] - prev_seq


def process(data):
    # part 1
    diffs = [solve(h) for h in data]
    part1 = sum(d[0] for d in diffs)
    print("part 1:", part1)
    # part 2
    part2 = sum(d[1] for d in diffs)
    print("part 2:", part2)


def parse_line(line):
    return list(map(int, line.split()))


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
