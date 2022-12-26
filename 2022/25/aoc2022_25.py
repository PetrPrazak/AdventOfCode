# https://adventofcode.com/2022/day/25
from pathlib import Path
import time


def snafu2int(snafu):
    total = 0
    radix = 1
    for c in reversed(snafu):
        i = -2 if c == "=" else -1 if c == "-" else int(c)
        total += i * radix
        radix *= 5
    return total


def int2snafu(num):
    out = ""
    while num:
        num, rem = divmod(num, 5)
        out += "012=-"[rem]
        num += rem > 2
    return out[::-1]


def process(data):
    result = sum(map(snafu2int, data))
    for snafu in data:
        s = int2snafu(snafu2int(snafu))
        assert s == snafu, f"{snafu}, {s}"
    print("part 1:", int2snafu(result))


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
