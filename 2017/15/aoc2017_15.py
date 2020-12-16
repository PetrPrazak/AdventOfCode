# http://adventofcode.com/2017/day/15
from __future__ import print_function

# Generator A starts with 873
# Generator B starts with 583


def gen(val, mult, mod=1):
    while 1:
        val = val * mult % 2147483647   # 2 ** 31 - 1
        if (val % mod) == 0:
            yield val & 0xFFFF


def checkgen(maxx, aval, bval, amod=1, bmod=1):
    genA = gen(aval, 16807, amod)
    genB = gen(bval, 48271, bmod)
    total = 0
    for _ in range(maxx):
        a, b = next(genA), next(genB)
        total += a == b
    return total


def solve():
    aval = 873
    bval = 583

    # test, part 1 = 588, part 2 = 309
    # aval = 65
    # bval = 8921

    # part 1
    print(checkgen(40000000, aval, bval))
    # part 2
    print(checkgen(5000000, aval, bval, 4, 8))


if __name__ == "__main__":
    solve()
