# https://adventofcode.com/2024/day/19
from pathlib import Path
from functools import cache
import time


def check_towels(towels, maxlen, pattern):
    @cache
    def matching(pattern):
        if not pattern:
            return 1
        return sum(matching(pattern[i:])
                   for i in range(1, min(maxlen, len(pattern))+1)
                   if pattern[:i] in towels)

    return matching(pattern)


def process(data):
    towels, patterns = data
    towels = set(towels)
    maxlen = max(map(len, towels))
    # part 1
    result = sum(check_towels(towels, maxlen, p) > 0 for p in patterns)
    print("part 1:", result)
    # part 2
    result = sum(check_towels(towels, maxlen, p) for p in patterns)
    print("part 2:", result)


def load_data(fileobj):
    towels, patterns = fileobj.read().split("\n\n")
    return towels.split(", "), patterns.split('\n')


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
