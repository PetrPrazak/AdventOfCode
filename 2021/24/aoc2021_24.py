# https://adventofcode.com/2021/day/24
from __future__ import print_function
from pprint import pprint
from pathlib import Path
from functools import lru_cache
from itertools import islice


def digit(D, z, divisor, add1, add2):
    # equivalent code from the input for a single digit
    x = (z % 26) + add1
    z //= divisor
    if x != D:
        z *= 26
        z += D + add2
    return z


@lru_cache(maxsize=None)
def check_digit(z, divisor, add1, add2):
    return {D: digit(D, z, divisor, add1, add2) for D in range(1, 10)}


@lru_cache(maxsize=None)
def compute(pos=0, z=0, last=True):
    if pos > 13:
        return "" if z == 0 else None
    d = check_digit(z, *PARAMS[pos])
    for num in sorted(d.keys(), reverse=last):
        rest = compute(pos+1, d[num], last)
        if rest is not None:
            return str(num) + rest


PARAMS = []


def process(data):
    # luckily all number sections are the same instructions long
    global PARAMS
    for i in range(14):
        part = data[i*18: (i+1) * 18]
        divisor = int(part[4][2])
        add1 = int(part[5][2])
        add2 = int(part[15][2])
        PARAMS.append((divisor, add1, add2))

    # part 1
    print("part 1:", compute())
    # part 2
    print("part 2:", compute(last=False))


def load_data(fileobj):
    return [line.strip().split() for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    main()
