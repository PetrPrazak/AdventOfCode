# replace 15 with day

"""

http://adventofcode.com/2017/day/15


"""

from __future__ import print_function


# Generator A starts with 873
# Generator B starts with 583


def gen(init, mult, mod, maxx):
    val = init
    for _ in range(maxx):
        while 1:
            val = val * mult % 2147483647
            if not mod or val % mod == 0:
                break
        yield val % 65536


def checkgen(aval, bval, amod, bmod, maxx):
    total = 0
    aiter = iter(gen(aval, 16807, amod, maxx))
    biter = iter(gen(bval, 48271, bmod, maxx))
    try:
        while 1:
            aval = next(aiter)
            bval = next(biter)
            if aval == bval:
                total += 1
    except StopIteration:
        pass
    return total


def solve():
    aval = 873
    bval = 583

    # test
    # aval = 65
    # bval = 8921

    # part 1
    print(checkgen(aval, bval, 0, 0, 40000000))

    # part 2
    print(checkgen(aval, bval, 4, 8, 5000000))


if __name__ == "__main__":
    solve()
