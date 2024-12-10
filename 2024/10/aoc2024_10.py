# https://adventofcode.com/2024/day/10
from pathlib import Path
from collections import defaultdict
import time


def walk(data, row, col, level=0, nines=None):
    if nines is None:
        nines = defaultdict(int)
    if not (0 <= row < len(data) and 0 <= col < len(data[0])):
        return nines
    num = data[row][col]
    if num != level:
        return nines
    if level == 9:
        nines[(row, col)] += 1
        return nines
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        walk(data, row + dr, col + dc, level + 1, nines)
    return nines


def process(data):
    zeros = [(r, c) for r, row in enumerate(data)
             for c, l in enumerate(row) if l == 0]
    # part 1
    walks = [walk(data, r, c) for r, c in zeros]
    result = sum(len(w) for w in walks)
    print("part 1:", result)
    # part 2
    result = sum(sum(v for v in w.values()) for w in walks)
    print("part 2:", result)


def load_data(fileobj):
    return [list(map(int,line.rstrip())) for line in fileobj.readlines()]


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
