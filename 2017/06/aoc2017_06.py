# https://adventofcode.com/2017/day/6
from __future__ import print_function


def solve(banks):
    passes = 0
    end = len(banks)
    states = set()
    states.add(tuple(banks))
    run = 1
    while 1:
        maxx = 0
        pos = 0
        for i in range(end):
            if banks[i] > maxx:
                pos = i
                maxx = banks[i]

        i = pos
        banks[i] = 0
        for _ in range(maxx):
            i += 1
            if i == end:
                i = 0
            banks[i] += 1

        passes += 1

        t = tuple(banks)
        if t in states:
            if run == 2:
                print(t)
                break
            states = set()
            states.add(t)
            passes = 0
            run = 2

        states.add(t)

    print(passes)


if __name__ == "__main__":
    with open("input.txt") as f:
        banks = [int(x) for x in f.readline().split()]
        solve(banks)
