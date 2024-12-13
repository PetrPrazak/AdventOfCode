# https://adventofcode.com/2024/day/13
from pathlib import Path
from math import floor
import re
import time


def find_tokens(buttonA_X, buttonA_Y, buttonB_X, buttonB_Y, prize_X, prize_Y):
    D = buttonA_X * buttonB_Y - buttonA_Y * buttonB_X
    A = prize_X * buttonB_Y - prize_Y * buttonB_X
    B = prize_Y * buttonA_X - prize_X * buttonA_Y
    return A/D, B/D


def count_tokens(data, inc=0):
    result = 0
    for d in data:
        d[4] += inc
        d[5] += inc
        A, B = find_tokens(*d)
        if floor(A) != A or floor(B) != B:
            continue
        result += int(A*3 + B)
    return result


def process(data):
    # part 1
    print("part 1:", count_tokens(data))
    # part 2
    inc = 10000000000000
    print("part 2:", count_tokens(data, inc))


def parse_section(section):
    return list(map(int, re.findall(f"\d+", section)))


def load_data(fileobj):
    return list(parse_section(part) for part in fileobj.read().split("\n\n"))


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
