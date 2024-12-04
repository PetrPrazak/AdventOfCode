# https://adventofcode.com/2024/day/1
from pathlib import Path
from collections import Counter
import time


def process(data):
    l1, l2 = zip(*data)
    result = sum(abs(p1-p2) for (p1, p2) in zip(sorted(l1), sorted(l2)))
    # part 1
    print("part 1:", result)
    # part 2
    c = Counter(l2)
    result = sum(p1 * c[p1] for p1 in l1)
    print("part 2:", result)


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
