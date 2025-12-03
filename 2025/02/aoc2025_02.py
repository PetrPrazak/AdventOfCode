# https://adventofcode.com/2025/day/2
from pathlib import Path
import time


def has_two_repeats(num):
    s = str(num)
    half, rem = divmod(len(s), 2)
    if rem == 1:
        return False
    return s[:half] == s[half:]


def has_atleast_two_repeats(num):
    s = str(num)
    half = len(s) // 2
    for r in range(half, 0, -1):
        first = s[:r]
        for rr in range(r, len(s), r):
            other = s[rr:rr + r]
            if other != first:
                break
        else:
            return True
    return False


def sum_repeats(data, cond):
    return sum(n if cond(n) else 0 for first, last in data for n in range(first, last+1))


def process(data):
    # part 1
    result = sum_repeats(data, has_two_repeats)
    print("part 1:", result)
    # part 2
    result = sum_repeats(data, has_atleast_two_repeats)
    print("part 2:", result)


def parse_range(section):
    first, last = section.rstrip().split('-')
    return int(first), int(last)


def load_data(fileobj):
    return list(parse_range(part) for part in fileobj.read().split(","))


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
