# https://adventofcode.com/2024/day/3
from pathlib import Path
from math import prod
import time
import re


def parse_mul(mul):
    return tuple(int(x) for x in mul.split(','))


def process(data):
    # part 1
    do = True
    part1 = part2 = 0
    for match in re.finditer(r"mul\((\d+,\d+)\)|(do)\(\)|(don't)\(\)", data):
        if mul := match.group(1):
            res = prod(parse_mul(mul))
            part1 += res
            if do:
                part2 += res
        if match.group(3):
            do = False
        elif match.group(2):
            do = True
    print("part 1:", part1)
    # part 2
    print("part 2:", part2)


def load_data(fileobj):
    return fileobj.read()


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
