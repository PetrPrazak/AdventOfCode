# https://adventofcode.com/2024/day/11
from pathlib import Path
from collections import defaultdict
from math import log10
import time


def process_stones(stones):
    newstones = defaultdict(int)
    for s, c in stones.items():
        if s == 0:
            newstones[1] += c
        else:
            w = int(log10(s) + 1)
            if w % 2 == 0:
                l, r = divmod(s, 10 ** (w // 2))
                newstones[l] += c
                newstones[r] += c
            else:
                newstones[s * 2024] += c
    return newstones


def solve(data, loops):
    stones = {s: 1 for s in data}
    for i in range(loops):
        stones = process_stones(stones)
    return sum(x for x in stones.values())


def process(data):
    # part 1
    result = solve(data, 25)
    print("part 1:", result)
    # part 2
    result = solve(data, 75)
    print("part 2:", result)


def load_data(fileobj):
    return list(map(int, fileobj.read().split()))


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
